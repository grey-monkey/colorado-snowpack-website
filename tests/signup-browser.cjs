const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const assert=require('node:assert/strict');const fs=require('node:fs');const path=require('node:path');
const base='http://127.0.0.1:8767/';
(async()=>{
const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
const out=path.resolve('work/signup-browser');fs.mkdirSync(out,{recursive:true});let count=0,mode='success';
const context=await browser.newContext({viewport:{width:1440,height:1000}});
// Contract-level UI simulations: no fixture address reaches Kit or Google.
await context.route('https://**/*',route=>{
 const url=route.request().url();
 if(url==='https://f.convertkit.com/ckjs/ck.5.js')return mode==='load-error'?route.abort():route.fulfill({contentType:'application/javascript',body:`document.querySelector('form').addEventListener('submit',async e=>{e.preventDefault();try{const r=await fetch('/signup-test',{method:'POST'});if(!r.ok)throw Error('provider failure');const el=document.createElement('div');el.className='formkit-alert-success';el.textContent='Check your inbox';e.target.append(el);}catch{e.target.querySelector('[data-element=errors]').textContent='PRIVATE PROVIDER ERROR';}});`});
 return route.abort();
});
const page=await context.newPage();
await page.route('**/signup-test',async route=>{count++;if(mode==='slow')await new Promise(r=>setTimeout(r,18000));if(mode==='network')return route.abort();return route.fulfill({status:mode==='error'?503:200,body:'{}'});});
async function open(){await page.goto(base+'weekly.html');await page.locator('button[type=submit]').waitFor();}
await open();await page.getByRole('button',{name:'Join the weekly'}).waitFor();
for(const width of [320,390,1440]){await page.setViewportSize({width,height:950});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);await page.screenshot({path:path.join(out,`signup-${width}.png`),fullPage:true});}
await page.getByLabel('Email address').fill('invalid');await page.getByRole('button',{name:'Join the weekly'}).click();assert.equal(count,0);
await page.getByLabel('Email address').fill('test@example.invalid');await page.getByLabel('Email address').press('Tab');assert.equal(await page.locator(':focus').textContent(),'Join the weekly');await page.keyboard.press('Enter');await page.getByText(/Check your inbox to confirm\. If/).waitFor();assert.equal(count,1);assert.equal(await page.getByRole('button',{name:'Join the weekly'}).isDisabled(),true);
for(mode of ['error','network']){await open();await page.getByLabel('Email address').fill('test@example.invalid');await page.getByRole('button',{name:'Join the weekly'}).click();await page.getByRole('alert').getByText(/could not complete/).waitFor();assert.doesNotMatch(await page.locator('body').textContent(),/PRIVATE PROVIDER ERROR/);assert.equal(await page.getByRole('button',{name:'Join the weekly'}).isEnabled(),true);}
mode='slow';await open();await page.getByLabel('Email address').fill('test@example.invalid');const before=count;await page.getByRole('button',{name:'Join the weekly'}).click();await page.getByText(/taking longer than usual/).waitFor({timeout:17000});assert.equal(count,before+1);assert.equal(await page.getByRole('button',{name:'Join the weekly'}).isDisabled(),true);await page.getByText(/Check your inbox to confirm\. If/).waitFor();
mode='load-error';await open();await page.getByText(/form could not load/).waitFor();assert.equal(await page.getByRole('button',{name:'Join the weekly'}).isDisabled(),true);
const touch=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});await touch.route('https://**/*',r=>r.abort());const tp=await touch.newPage();await tp.goto(base+'weekly.html');await tp.getByLabel('Email address').tap();assert.equal(await tp.locator(':focus').getAttribute('type'),'email');await touch.close();
console.log('PASS: 320/390/1440 widths, keyboard/touch, invalid email, success/duplicate guard, provider/network/script failure, slow response; all external test submissions blocked.');
await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1});
