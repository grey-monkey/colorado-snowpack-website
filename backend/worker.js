// No request bodies, addresses, credentials or provider responses are logged.
const SUCCESS='Check your inbox to confirm your subscription. If you already subscribe, you are all set.';
const UNAVAILABLE='Signup is temporarily unavailable. Please try again later.';
const encoder=new TextEncoder();
const json=(body,status=200)=>Response.json(body,{status,headers:{'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}});
export async function digest(secret,value){
 const key=await crypto.subtle.importKey('raw',encoder.encode(secret),{name:'HMAC',hash:'SHA-256'},false,['sign']);
 return Array.from(new Uint8Array(await crypto.subtle.sign('HMAC',key,encoder.encode(value))),x=>x.toString(16).padStart(2,'0')).join('');
}
export async function readSmall(request){
 if(Number(request.headers.get('content-length'))>2048)throw Error('large');
 const reader=request.body?.getReader();if(!reader)throw Error('empty');
 let size=0,text='';const decoder=new TextDecoder();
 while(true){const {done,value}=await reader.read();if(done)break;size+=value.length;if(size>2048){await reader.cancel();throw Error('large');}text+=decoder.decode(value,{stream:true});}
 return JSON.parse(text+decoder.decode());
}
export async function signup(request,env){
 if(!['private','public'].includes(env.SIGNUP_MODE)||!env.KIT_API_KEY||!env.HASH_SECRET||!/^\d+$/.test(env.KIT_FORM_ID||'')||!/^\d+$/.test(env.KIT_TAG_ID||''))return json({message:UNAVAILABLE},503);
 let body;try{body=await readSmall(request);}catch{return json({message:'Please enter a valid email address.'},400);}
 if(!body||Array.isArray(body)||typeof body.email!=='string'||typeof body.website!=='string'||Object.keys(body).some(k=>!['email','website'].includes(k)))return json({message:'Please enter a valid email address.'},400);
 const email=body.email.trim().toLowerCase();
 if(email.length>254||! /^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/.test(email))return json({message:'Please enter a valid email address.'},400);
 if(body.website)return json({message:SUCCESS}); // Honeypot: no provider call.
 if(env.SIGNUP_MODE==='private'&&email!==(env.TEST_EMAIL||'').toLowerCase())return json({message:'This preview accepts only the approved private test address.'},403);
 const ip=request.headers.get('CF-Connecting-IP');if(!ip)return json({message:UNAVAILABLE},503);
 const keys={email:await digest(env.HASH_SECRET,'email:'+email),ip:await digest(env.HASH_SECRET,'ip:'+ip)};
 const gate=env.GUARD.get(env.GUARD.idFromName('signup'));
 const decision=await (await gate.fetch('https://internal/reserve',{method:'POST',body:JSON.stringify(keys)})).json();
 if(decision.duplicate)return json({message:'A request was made recently. Check your inbox before trying again in an hour.',recent:true});
 if(!decision.allowed)return json({message:'Too many attempts. Please wait an hour before trying again.'},429);
 try{
  const options={method:'POST',headers:{'X-Kit-Api-Key':env.KIT_API_KEY,'Content-Type':'application/json'},signal:AbortSignal.timeout(10000)};
  // Never create an active subscriber or override a cancellation.
  const create=await fetch('https://api.kit.com/v4/subscribers',{...options,body:JSON.stringify({email_address:email,state:'inactive'})});
  if(!create.ok)throw Error('provider');
  const {subscriber}=await create.json();
  if(!subscriber||!Number.isInteger(subscriber.id))throw Error('provider');
  if(['cancelled','complained','bounced'].includes(subscriber.state)){
   return json({message:'This address is unsubscribed or cannot receive email. Please use the original Kit confirmation form to request rejoining.',rejoin:true});
  }
  const tag=await fetch(`https://api.kit.com/v4/tags/${env.KIT_TAG_ID}/subscribers/${subscriber.id}`,{...options,signal:AbortSignal.timeout(10000),body:'{}'});
  if(!tag.ok)throw Error('provider');
  const add=await fetch(`https://api.kit.com/v4/forms/${env.KIT_FORM_ID}/subscribers/${subscriber.id}`,{...options,signal:AbortSignal.timeout(10000),body:JSON.stringify({referrer:env.SITE_ORIGIN})});
  if(!add.ok)throw Error('provider');
  return json({message:SUCCESS});
 }catch{
  // Keep reservation even on timeout: Kit may already have accepted it.
  return json({message:'We could not confirm the request. Check your inbox before trying again in an hour.'},503);
 }
}
export default {async fetch(request,env){
 const url=new URL(request.url);
 if(url.pathname==='/internal/weekly'){
  if(!env.AUTOMATION_SECRET||request.headers.get('Authorization')!==`Bearer ${env.AUTOMATION_SECRET}`)return json({message:'Not found'},404);
  if(!['enabled','private'].includes(env.NEWSLETTER_MODE)||request.method!=='POST')return json({message:'Weekly sending is disabled.'},503);
  try{return await env.EDITIONS.get(env.EDITIONS.idFromName('weekly')).fetch(request);}catch{return json({message:'Delivery status is uncertain; reconcile before retrying.'},503);}
 }
 if(url.pathname!=='/api/signup')return env.ASSETS?env.ASSETS.fetch(request):new Response('Not found',{status:404});
 const origin=request.headers.get('Origin');
 const allowed=(env.ALLOWED_ORIGINS||'').split(',').includes(origin);
 if(!allowed)return json({message:'Please use the signup form on our website.'},403);
 const cors={'Access-Control-Allow-Origin':origin,'Vary':'Origin','Access-Control-Allow-Methods':'POST, OPTIONS','Access-Control-Allow-Headers':'Content-Type'};
 let response;
 if(request.method==='OPTIONS')response=new Response(null,{status:204});
 else if(request.method!=='POST')response=json({message:'Please use the signup form.'},405);
 else if(!request.headers.get('Content-Type')?.startsWith('application/json'))response=json({message:'Please use the signup form.'},415);
 else try{response=await signup(request,env);}catch{response=json({message:UNAVAILABLE},503);}
 const safe=new Response(response.body,response);for(const [k,v]of Object.entries(cors))safe.headers.set(k,v);return safe;
}};

// A single SQLite-backed object makes reservations atomic across all regions.
// Only HMAC digests and short-lived counters are retained, not subscriber records.
export class SignupGuard {
 constructor(ctx){this.ctx=ctx;this.sql=ctx.storage.sql;this.sql.exec('CREATE TABLE IF NOT EXISTS limits (key TEXT PRIMARY KEY, count INTEGER NOT NULL, expires INTEGER NOT NULL)');}
 async fetch(request){
  const {email,ip}=await request.json();
  if(!/^[a-f0-9]{64}$/.test(email)||!/^[a-f0-9]{64}$/.test(ip))return json({allowed:false},400);
  const now=Date.now();let result;
  this.ctx.storage.transactionSync(()=>{
   this.sql.exec('DELETE FROM limits WHERE expires <= ?',now);
   const count=key=>this.sql.exec('SELECT count FROM limits WHERE key=?',key).toArray()[0]?.count||0;
   const ipKey='ip:'+ip,mailKey='email:'+email,dayKey='day:'+Math.floor(now/86400000);
   if(count(ipKey)>=6){result={allowed:false};return;}
   this.sql.exec('INSERT INTO limits VALUES (?,1,?) ON CONFLICT(key) DO UPDATE SET count=count+1',ipKey,now+3600000);
   if(count(mailKey)){result={duplicate:true};return;}
   if(count(dayKey)>=100){result={allowed:false};return;}
   this.sql.exec('INSERT INTO limits VALUES (?,1,?)',mailKey,now+3600000);
   this.sql.exec('INSERT INTO limits VALUES (?,1,?) ON CONFLICT(key) DO UPDATE SET count=count+1',dayKey,(Math.floor(now/86400000)+1)*86400000);
   result={allowed:true};
  });
  await this.ctx.storage.setAlarm(now+3600000);
  return json(result);
 }
 async alarm(){this.sql.exec('DELETE FROM limits WHERE expires <= ?',Date.now());if(this.sql.exec('SELECT key FROM limits LIMIT 1').toArray().length)await this.ctx.storage.setAlarm(Date.now()+3600000);}
}

// Durable pre-send reservation survives runner restarts, redeploys and timeouts.
export class EditionLedger {
 constructor(ctx,env){this.ctx=ctx;this.env=env;this.sql=ctx.storage.sql;this.sql.exec('CREATE TABLE IF NOT EXISTS editions (edition TEXT PRIMARY KEY, state TEXT, broadcast_id INTEGER, created TEXT)');}
 async fetch(request){
  const env=this.env;
  if(!['enabled','private'].includes(env.NEWSLETTER_MODE)||!env.KIT_API_KEY||!/^\d+$/.test(env.KIT_TAG_ID||'')||!/^\d+$/.test(env.KIT_TEMPLATE_ID||'')||! /^[^@\s]+@coloradosnowpack\.com$/.test(env.SENDER_EMAIL||''))return json({message:'Sending configuration is incomplete.'},503);
  // Payload is generated by the accepted-history workflow, never public input.
  if(Number(request.headers.get('content-length'))>40000)return json({message:'Invalid edition'},400);
  const text=await request.text();if(text.length>40000)return json({message:'Invalid edition'},400);
  let e;try{e=JSON.parse(text);}catch{return json({message:'Invalid edition'},400);}
  const age=Date.now()-Date.parse(e?.facts?.end+'T00:00:00Z');
  if(!/^snowpack-weekly:\d{4}-W\d{2}$/.test(e?.key)||!Number.isFinite(age)||age<0||age>3*86400000||!e.facts.delivery_eligible||typeof e.content!=='string'||e.content.length>30000||typeof e.subject!=='string'||e.subject.length>180)return json({message:'Invalid or stale edition'},400);
  if(env.NEWSLETTER_MODE==='private'){
   // The hosted proof can reach exactly one approved active recipient.
   try{
    const check=await fetch(`https://api.kit.com/v4/tags/${env.KIT_TAG_ID}/subscribers`,{headers:{'X-Kit-Api-Key':env.KIT_API_KEY},signal:AbortSignal.timeout(10000)});
    if(!check.ok)throw Error('provider');
    const members=await check.json(),s=members.subscribers;
    if(!env.TEST_EMAIL||members.pagination?.has_next_page||!Array.isArray(s)||s.length!==1||s[0].state!=='active'||s[0].email_address?.toLowerCase()!==env.TEST_EMAIL.toLowerCase())return json({message:'Private recipient is not ready.'},409);
   }catch{return json({message:'Private recipient could not be verified.'},503);}
   e.key+=':private';
   e.subject='[Private hosted proof] '+e.subject;
  }
  let duplicate=false;
  this.ctx.storage.transactionSync(()=>{
   duplicate=this.sql.exec('SELECT edition FROM editions WHERE edition=?',e.key).toArray().length>0;
   if(!duplicate)this.sql.exec('INSERT INTO editions VALUES (?,?,NULL,?)',e.key,'reserved',new Date().toISOString());
  });
  if(duplicate)return json({message:'Edition already reserved. No resend.'},409);
  try{
   const response=await fetch('https://api.kit.com/v4/broadcasts',{method:'POST',headers:{'X-Kit-Api-Key':env.KIT_API_KEY,'Content-Type':'application/json'},signal:AbortSignal.timeout(20000),body:JSON.stringify({email_template_id:Number(env.KIT_TEMPLATE_ID),email_address:env.SENDER_EMAIL,subject:e.subject,description:e.key,content:e.content,public:false,send_at:new Date().toISOString(),subscriber_filter:[{all:[{type:'tag',ids:[Number(env.KIT_TAG_ID)]}]}]})});
   if(!response.ok)throw Error('provider');
   const {broadcast}=await response.json();if(!Number.isInteger(broadcast?.id))throw Error('provider');
   this.sql.exec('UPDATE editions SET state=?,broadcast_id=? WHERE edition=?',broadcast.status,broadcast.id,e.key);
   return json({edition:e.key,broadcast_id:broadcast.id,status:broadcast.status});
  }catch{return json({message:'Edition reserved; delivery uncertain. Reconcile in Kit before any retry.'},503);}
 }
}
