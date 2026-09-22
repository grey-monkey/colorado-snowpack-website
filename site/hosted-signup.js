const box=document.querySelector('[data-hosted-signup]');
if(box){
 const form=box.querySelector('form'),button=form.querySelector('button'),status=box.querySelector('.signup-status');
 let busy=false,done=false;
 button.disabled=false;status.textContent='One email a week. Confirm your subscription in your inbox.';
 form.addEventListener('submit',async event=>{
  event.preventDefault();if(busy||done||!form.checkValidity())return;
  busy=true;button.disabled=true;form.setAttribute('aria-busy','true');status.textContent='Sending your request…';
  const timer=setTimeout(()=>{status.textContent='This is taking longer than usual. Please wait and check your inbox before trying again.';},8000);
  try{
   const response=await fetch(form.dataset.endpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:form.elements.email.value,website:form.elements.website.value}),signal:AbortSignal.timeout(25000),credentials:'omit',referrerPolicy:'no-referrer'});
   const result=await response.json();
   // Fixed copy only; never render raw backend/provider responses.
   if(response.ok){
    status.textContent=result.rejoin?'If you previously unsubscribed, request a new confirmation using the link below.':result.recent?'A request was made recently. Check your inbox before trying again in an hour.':'Check your inbox to confirm your subscription. If you already subscribe, you are all set.';
    box.querySelector('.signup-rejoin').hidden=!result.rejoin;done=true;form.elements.email.value='';
   }else if(response.status===400)status.textContent='Please check your email address and try again.';
   else if(response.status===429)status.textContent='Too many attempts. Please wait an hour before trying again.';
   else if(response.status===403)status.textContent='This preview accepts only the approved private test address.';
   else status.textContent='Signup is temporarily unavailable. Check your inbox before trying again later.';
  }catch{status.textContent='We could not confirm the request. Check your inbox before trying again later.';}
  finally{clearTimeout(timer);busy=false;button.disabled=done;form.removeAttribute('aria-busy');}
 });
}
