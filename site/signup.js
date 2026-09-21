// Kit owns submission, confirmation, CAPTCHA and subscriber records.
const box=document.querySelector('[data-signup]');
if(box){
 const form=box.querySelector('form'),button=form.querySelector('button[type=submit]'),status=box.querySelector('.signup-status');
 let busy=false,settled=false,slow;
 function observeResult(){
  const success=form.querySelector('.formkit-alert-success');
  const errors=form.querySelector('[data-element=errors]');
  if(success){success.setAttribute('role','status');status.textContent='Check your inbox to confirm. If you already subscribe, you are all set.';busy=false;settled=true;clearTimeout(slow);button.disabled=true;form.removeAttribute('aria-busy');}
  else if(errors?.textContent.trim()){
   const safe='We could not complete signup. Please check your email address and try again in a moment.';
   if(errors.textContent!==safe)errors.textContent=safe;
   status.textContent='Your subscription has not been confirmed.';busy=false;clearTimeout(slow);button.disabled=false;form.removeAttribute('aria-busy');
  }
 }
 new MutationObserver(observeResult).observe(form,{childList:true,subtree:true});
 form.addEventListener('submit',event=>{
  if(busy||settled){event.preventDefault();event.stopImmediatePropagation();return;}
  if(!form.checkValidity())return;
  busy=true;button.disabled=true;form.setAttribute('aria-busy','true');status.textContent='Sending your request…';
  slow=setTimeout(()=>{if(busy)status.textContent='This is taking longer than usual. Please wait and check your inbox before trying again. If no confirmation arrives, reload this page to retry.';},15000);
 },true);
 const script=document.createElement('script');script.src='https://f.convertkit.com/ckjs/ck.5.js';
 const loadTimer=setTimeout(()=>{status.textContent='The signup form could not load. Please reload the page in a moment.';},15000);
 script.onload=()=>{clearTimeout(loadTimer);button.disabled=false;status.textContent='One email a week. Confirm your subscription in your inbox.';};
 script.onerror=()=>{clearTimeout(loadTimer);status.textContent='The signup form could not load. Please reload the page in a moment.';};
 document.head.append(script);
}
