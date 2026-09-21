const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 try{
 const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(String(e)));
 await page.goto('http://127.0.0.1:8765');await page.locator('#dashboard').waitFor({state:'visible'});
 assert.match(await page.locator('#snapshot-status').textContent(),/Latest available snapshot/);
 const dataPath=await page.locator('body').getAttribute('data-snapshot');assert.match(dataPath,/data\/releases\/\d+\/snapshot.json/);
 const snap=await (await page.request.get('http://127.0.0.1:8765/'+dataPath)).json();
 const exports=await (await page.request.get('http://127.0.0.1:8765/'+dataPath.replace('snapshot.json','series.json'))).json();
 assert.equal(exports.metadata.release_id,snap.release_id);assert.equal(exports.observations.length,29567);
 const swe=await page.locator('#swe').textContent();assert.equal(swe,'0.04');
 await page.route('**/data/health.json',r=>r.fulfill({json:{status:'validation_failed',release_id:snap.release_id}}));
 await page.reload();await page.getByText(/latest update could not be completed/).waitFor();assert.equal(await page.locator('#swe').textContent(),swe);
 await page.unroute('**/data/health.json');await page.route('**/data/health.json',r=>r.abort());await page.reload();await page.locator('#dashboard').waitFor({state:'visible'});assert.equal(await page.locator('#swe').textContent(),swe);
 await page.unroute('**/data/health.json');await page.reload();await page.locator('#dashboard').waitFor({state:'visible'});assert.doesNotMatch(await page.locator('#snapshot-status').textContent(),/could not/);
 assert.deepEqual(errors,[]);console.log('PASS: real accepted release, matching exports, retained readings after failed update, unavailable health file, recovery');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
