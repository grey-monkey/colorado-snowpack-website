const {chromium}=require('C:/Users/grey/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
(async()=>{
const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
const page=await browser.newPage();let mode='ok',count=0;
await page.route('https://**/*',r=>r.abort());
await page.route('**/api/signup',async r=>{count++;if(mode==='network')return r.abort();if(mode==='slow')await new Promise(resolve=>setTimeout(resolve,9000));await r.fulfill({status:mode==='error'?503:mode==='limit'?429:200,contentType:'application/json',body:JSON.stringify({message:'PRIVATE PROVIDER TRACE',recent:mode==='recent',rejoin:mode==='rejoin'})});});
fs.mkdirSync('work/hosted-browser',{recursive:true});
async function open(){await page.goto('http://127.0.0.1:8768/weekly.html');await page.getByRole('button',{name:'Join the weekly'}).waitFor();}
await open();
for(const width of [320,390,1440]){await page.setViewportSize({width,height:900});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);await page.screenshot({path:`work/hosted-browser/signup-${width}.png`,fullPage:true});}
await page.getByLabel('Email address').fill('invalid');await page.getByRole('button',{name:'Join the weekly'}).click();assert.equal(count,0);
for(mode of ['ok','error','network','limit','slow','recent','rejoin']){
 await open();await page.getByLabel('Email address').fill('test@example.invalid');await page.getByLabel('Email address').press('Tab');assert.equal(await page.locator(':focus').textContent(),'Join the weekly');const before=count;await page.keyboard.press('Enter');
 if(mode==='slow'){await page.getByRole('status').getByText(/taking longer/).waitFor({timeout:10000});assert.equal(await page.getByRole('button',{name:'Join the weekly'}).isDisabled(),true);}
 const expected=mode==='error'?/temporarily unavailable/:mode==='network'?/could not confirm/:mode==='limit'?/Too many attempts/:mode==='recent'?/made recently/:mode==='rejoin'?/previously unsubscribed/:/Check your inbox/;
 await page.getByRole('status').getByText(expected).waitFor();assert.equal(count,before+1);assert.doesNotMatch(await page.locator('body').textContent(),/PRIVATE PROVIDER TRACE/);
}
const touch=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});const tp=await touch.newPage();await tp.goto('http://127.0.0.1:8768/weekly.html');await tp.getByLabel('Email address').tap();assert.equal(await tp.locator(':focus').getAttribute('name'),'email');await touch.close();
console.log('PASS: hosted-form responsive/keyboard/touch and simulated invalid/success/error/offline/rate-limit/slow/recent/rejoin states. No real emails submitted.');await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1;});
