import {test} from 'node:test';
import assert from 'node:assert/strict';
import {DatabaseSync} from 'node:sqlite';
import worker,{SignupGuard,EditionLedger} from '../backend/worker.js';

function fixture(){
 const db=new DatabaseSync(':memory:');
 const storage={sql:{exec(query,...args){const s=db.prepare(query);if(!query.startsWith('SELECT'))s.run(...args);return{toArray:()=>s.all(...args)};}},transactionSync(fn){db.exec('BEGIN IMMEDIATE');try{fn();db.exec('COMMIT');}catch(e){db.exec('ROLLBACK');throw e;}},async setAlarm(){}};
 const guard=new SignupGuard({storage});
 const env={SIGNUP_MODE:'private',TEST_EMAIL:'test@example.invalid',KIT_API_KEY:'secret-not-public',KIT_FORM_ID:'1',KIT_TAG_ID:'2',HASH_SECRET:'long-test-secret',ALLOWED_ORIGINS:'https://example.invalid',SITE_ORIGIN:'https://example.invalid',GUARD:{idFromName:x=>x,get:()=>({fetch:(url,opts)=>guard.fetch(new Request(url,opts))})}};
 const request=(body={email:'test@example.invalid',website:''},headers={})=>new Request('https://example.invalid/api/signup',{method:'POST',headers:{Origin:'https://example.invalid','Content-Type':'application/json','CF-Connecting-IP':'192.0.2.1',...headers},body:typeof body==='string'?body:JSON.stringify(body)});
 return{db,env,request,storage};
}
test('hosted signup validation, provider failure and abuse limits',async()=>{
 const original=globalThis.fetch;let calls=0,mode='normal';
 globalThis.fetch=async(url,opts)=>{calls++;assert.equal(opts.headers['X-Kit-Api-Key'],'secret-not-public');if(mode==='failure')return new Response('secret stack trace',{status:500});if(url.endsWith('/subscribers'))assert.equal(JSON.parse(opts.body).state,'inactive');return Response.json({subscriber:{id:1,state:mode==='cancelled'?'cancelled':'inactive'}});};
 try{
  const {db,env,request}=fixture();
  for(const body of ['{',null,{email:'bad',website:''},{email:'test@example.invalid',website:'',extra:'bad'}])assert.equal((await worker.fetch(request(body),env)).status,400);
  assert.equal((await worker.fetch(request(undefined,{Origin:'https://evil.invalid'}),env)).status,403);
  assert.equal((await worker.fetch(request({email:'someone@example.invalid',website:''}),env)).status,403);
  assert.equal((await worker.fetch(request(' '.repeat(3000)),env)).status,400);
  assert.equal((await worker.fetch(request({email:'test@example.invalid',website:'spam'}),env)).status,200);assert.equal(calls,0);
  const first=await worker.fetch(request(),env);assert.equal(first.status,200);assert.doesNotMatch(await first.text(),/secret|subscriber|192\.0/);assert.equal(calls,3);
  for(let i=0;i<5;i++)await worker.fetch(request(),env);
  assert.equal((await worker.fetch(request(),env)).status,429);assert.equal(calls,3);
  const rows=db.prepare('SELECT key FROM limits').all();assert.ok(rows.length);assert.ok(rows.every(x=>!x.key.includes('@')&&!x.key.includes('192.')));db.close();
  for(const failure of ['failure','cancelled']){
   mode=failure;const f=fixture(),before=calls;const result=await worker.fetch(f.request(),f.env);assert.equal(result.status,failure==='failure'?503:200);assert.doesNotMatch(await result.text(),/secret|stack/);await worker.fetch(f.request(),f.env);assert.equal(calls,before+1);f.db.close();
  }
  const f=fixture();f.env.GUARD.get=()=>{throw Error('storage unavailable')};assert.equal((await worker.fetch(f.request(),f.env)).status,503);f.db.close();
  mode='normal';const g=fixture();g.env.SIGNUP_MODE='public';
  for(let i=0;i<100;i++)assert.equal((await worker.fetch(g.request({email:`person${i}@example.invalid`,website:''},{'CF-Connecting-IP':`192.0.2.${i}`}),g.env)).status,200);
  const before=calls;assert.equal((await worker.fetch(g.request({email:'last@example.invalid',website:''},{'CF-Connecting-IP':'192.0.2.200'}),g.env)).status,429);assert.equal(calls,before);g.db.close();
 }finally{globalThis.fetch=original;}
});
test('weekly reservation persists through success, restart and uncertain provider response',async()=>{
 const original=globalThis.fetch;
 try{for(const failure of [false,true]){
  const f=fixture();let calls=0;
  Object.assign(f.env,{NEWSLETTER_MODE:'enabled',KIT_TEMPLATE_ID:'1',SENDER_EMAIL:'hello@coloradosnowpack.com'});
  globalThis.fetch=async()=>{calls++;if(failure)throw Error('timeout');return Response.json({broadcast:{id:123,status:'sending'}});};
  let ledger=new EditionLedger({storage:f.storage},f.env);
  const request=()=>new Request('https://internal/weekly',{method:'POST',body:JSON.stringify({key:'snowpack-weekly:2026-W39',facts:{end:new Date().toISOString().slice(0,10),delivery_eligible:true},subject:'Weekly',content:'<p>Facts</p>'})});
  assert.equal((await ledger.fetch(request())).status,failure?503:200);
  ledger=new EditionLedger({storage:f.storage},f.env);
  assert.equal((await ledger.fetch(request())).status,409);assert.equal(calls,1);f.db.close();
 }}finally{globalThis.fetch=original;}
});

test('private hosted delivery requires exactly the approved active recipient',async()=>{
 const original=globalThis.fetch;
 try{for(const kind of ['wrong','inactive','extra','pagination','unavailable','ready']){
  const f=fixture();let sends=0;
  Object.assign(f.env,{NEWSLETTER_MODE:'private',KIT_TEMPLATE_ID:'1',SENDER_EMAIL:'hello@coloradosnowpack.com'});
  globalThis.fetch=async(url,options)=>{
   if(url.endsWith('/broadcasts')){sends++;const b=JSON.parse(options.body);assert.equal(b.email_address,'hello@coloradosnowpack.com');assert.equal(b.public,false);return Response.json({broadcast:{id:123,status:'sending'}});}
   if(kind==='unavailable')throw Error('offline');
   const member={email_address:kind==='wrong'?'other@example.invalid':f.env.TEST_EMAIL,state:kind==='inactive'?'inactive':'active'};
   return Response.json({subscribers:kind==='extra'?[member,member]:[member],pagination:{has_next_page:kind==='pagination'}});
  };
  const ledger=new EditionLedger({storage:f.storage},f.env);
  const request=()=>new Request('https://internal/weekly',{method:'POST',body:JSON.stringify({key:'snowpack-weekly:2026-W39',facts:{end:new Date().toISOString().slice(0,10),delivery_eligible:true},subject:'Weekly',content:'<p>Facts</p>'})});
  assert.equal((await ledger.fetch(request())).status,kind==='ready'?200:kind==='unavailable'?503:409);
  assert.equal(sends,kind==='ready'?1:0);
  if(kind==='ready'){assert.equal((await ledger.fetch(request())).status,409);assert.equal(sends,1);assert.equal(f.db.prepare('SELECT edition FROM editions').get().edition,'snowpack-weekly:2026-W39:private');}
  f.db.close();
 }}finally{globalThis.fetch=original;}
});
