const {chromium}=require('C:/Users/grey/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const assert=require('node:assert/strict');
(async()=>{const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});try{
const p=await browser.newPage();const base=process.env.SITE_URL||'http://127.0.0.1:8765';await p.goto(base);await p.locator('#dashboard').waitFor({state:'visible'});const snapshot=await(await p.request.get(base+'/'+await p.locator('body').getAttribute('data-snapshot'))).json();assert.equal(snapshot.regions.length,9);assert.equal(await p.locator('#region optgroup').count(),5);
for(const width of [320,390,768,1440]){
 await p.setViewportSize({width,height:900});await p.evaluate(()=>document.fonts.ready);
 for(const r of snapshot.regions){
  await p.selectOption('#region',r.id);assert.equal(new URL(p.url()).searchParams.get('region'),r.id);assert.equal(await p.locator('#source').getAttribute('href'),r.source);assert((await p.locator('#chart-title').textContent()).includes(r.name));
  const value=r.years['2026'][r.dates.indexOf('09-21')];const expected=value===0?'0.00':value<.005?'<0.005':value.toFixed(2);assert.equal(await p.locator('#swe').textContent(),expected);
  assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  const fits=await p.locator('#region').evaluate(el=>{const c=document.createElement('canvas').getContext('2d'),s=getComputedStyle(el);c.font=s.font;return c.measureText(el.selectedOptions[0].textContent).width+parseFloat(s.paddingLeft)+parseFloat(s.paddingRight)<=el.clientWidth;});assert(fits,'Full basin name fits at '+width+': '+r.name);
 }
}
await p.goto(base+'/?region=co-gunnison&year=2025');await p.locator('#dashboard').waitFor({state:'visible'});assert.equal(await p.locator('#region').inputValue(),'co-gunnison');assert.equal(await p.locator('#season').inputValue(),'2025');await p.locator('.overview').screenshot({path:'../../outputs/ColoradoSnowpack-basin-card.png'});
console.log('Passed: all nine views at four widths; grouped menu, exact readings, source links, chart titles, full names, and shared region/year links.');
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
