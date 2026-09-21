// Development-only browser checks. Injected scenarios never enter public files.
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const base='http://127.0.0.1:8765';
const output=path.resolve(process.argv[2]||'work/browser');fs.mkdirSync(output,{recursive:true});
const report={checks:[],errors:[]};
const check=(name)=>report.checks.push(name);
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.BROWSER_EXE||'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const context=await browser.newContext({viewport:{width:1440,height:1000}});
 const page=await context.newPage();page.on('pageerror',e=>report.errors.push(String(e)));
 await page.goto(base);await page.locator('#dashboard').waitFor({state:'visible'});
 assert.equal(await page.locator('#swe').textContent(),'0.04');assert.match(await page.locator('#condition-copy').textContent(),/median is zero/);assert.match(await page.locator('#snapshot-status').textContent(),/Frozen/);check('Real September source values and frozen/zero-median labels');
 await page.screenshot({path:path.join(output,'desktop.png'),fullPage:true});
 await page.locator('#region').selectOption('co-colorado-headwaters');assert.equal(await page.locator('#swe').textContent(),'0.05');assert.match(page.url(),/region=co-colorado-headwaters/);
 await page.reload();await page.locator('#dashboard').waitFor({state:'visible'});assert.equal(await page.locator('#region').inputValue(),'co-colorado-headwaters');check('Region selection coordinates chart/readout and persists in bookmark URL');
 await page.locator('#season').selectOption('2024');await page.locator('#day').fill('151');assert.match(await page.locator('#date-reading').textContent(),/February 29, 2024/);await page.locator('#season').selectOption('2025');assert.match(await page.locator('#date-reading').textContent(),/no calendar date/);check('Actual leap-year and non-leap-year chart inspection');
 await page.locator('#day').focus();const before=Number(await page.locator('#day').inputValue());await page.keyboard.press('ArrowRight');assert.equal(Number(await page.locator('#day').inputValue()),before+1);check('Keyboard slider changes date and has accessible value text');
 await page.locator('summary').click();assert.equal(await page.locator('#table-body tr').count(),366);check('Accessible numerical table with 366 month/day positions');
 await page.goto(base);await page.locator('#dashboard').waitFor({state:'visible'});await page.keyboard.press('Tab');assert.equal(await page.locator(':focus').textContent(),'Skip to content');await page.keyboard.press('Enter');assert.equal(await page.locator(':focus').getAttribute('id'),'main');check('Skip link moves keyboard focus into main');
 for(const width of [320,390,768,1440]){await page.setViewportSize({width,height:900});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,`overflow at ${width}`);}check('No horizontal page overflow at 320/390/768/1440px');
 const touch=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:1});const mobile=await touch.newPage();await mobile.goto(base);await mobile.locator('#dashboard').waitFor({state:'visible'});await mobile.screenshot({path:path.join(output,'mobile.png'),fullPage:true});await mobile.locator('summary').tap();assert.equal(await mobile.locator('#table-details').getAttribute('open'),'');await mobile.locator('#day').tap();check('Mobile touch can open table and interact with date slider');
 for(const file of ['methods.html','weekly.html','privacy.html','data/series.csv','data/series.json','data/metadata.json','favicon.svg','sitemap.xml']){const r=await page.request.get(base+'/'+file);assert.equal(r.status(),200,file);}check('All information pages and public downloads return successfully');
 const exported=await (await page.request.get(base+'/data/series.json')).json();assert.equal(exported.observations.length,29585);assert.equal(exported.observations.find(r=>r.region_id==='co-state'&&r.observation_date==='2026-09-21').swe_inches,.0443478261);check('Public export matches verified observations and displayed value');
 const snapshot=await (await page.request.get(base+'/data/snapshot.json')).json();
 const scenarios=[
  ['normal winter','2026-02-01',8,10,/80%/],
  ['measured zero','2026-02-01',0,10,/0%/],
  ['missing observation','2026-02-01',null,10,/unavailable/],
  ['missing reference','2026-02-01',1,null,/unavailable/],
  ['near-zero reference','2026-09-21',.02,.05,/quiet/]
 ];
 for(const [name,date,swe,median,expected]of scenarios){const fixture=structuredClone(snapshot);fixture.observation_date=date;const r=fixture.regions[0],i=r.dates.indexOf(date.slice(5));r.years['2026'][i]=swe;r.median[i]=median;await page.route('**/data/snapshot.json',route=>route.fulfill({json:fixture}));await page.goto(base);await page.locator('#dashboard').waitFor({state:'visible'});assert.match(await page.locator('#condition-title').textContent(),expected,name);await page.unroute('**/data/snapshot.json');check('Simulated UI: '+name);}
 const old=structuredClone(snapshot);old.observation_date='2024-09-21';old.status='accepted';await page.route('**/data/snapshot.json',r=>r.fulfill({json:old}));await page.goto(base);await page.locator('#dashboard').waitFor({state:'visible'});assert.match(await page.locator('#snapshot-status').textContent(),/overdue/);await page.unroute('**/data/snapshot.json');check('Simulated stale automated snapshot visibly warns');
 let release;const held=new Promise(r=>release=r);await page.route('**/data/snapshot.json',async r=>{await held;await r.fulfill({status:503,body:'Unavailable'});});await page.goto(base);assert.match(await page.locator('#snapshot-status').textContent(),/Loading/);assert.equal(await page.locator('#dashboard').isVisible(),false);release();await page.locator('#load-error').waitFor({state:'visible'});await page.unroute('**/data/snapshot.json');await page.locator('#retry').click();await page.locator('#dashboard').waitFor({state:'visible'});check('Simulated loading, service failure, and successful retry');
 await page.route('**/data/snapshot.json',r=>r.fulfill({json:{schema_version:'broken'}}));await page.goto(base);await page.locator('#load-error').waitFor({state:'visible'});assert.equal(await page.locator('#dashboard').isVisible(),false);check('Malformed snapshots fail closed without displaying measurements');
 assert.deepEqual(report.errors,[]);check('No browser page errors');
 await browser.close();fs.writeFileSync(path.join(output,'report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
})().catch(e=>{console.error(e);process.exit(1)});
