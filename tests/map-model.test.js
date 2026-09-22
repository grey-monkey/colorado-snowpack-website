import test from 'node:test';
import assert from 'node:assert/strict';
import {reading,metricFor,fillFor,displayReading} from '../site/map-model.js';
import fs from 'node:fs';
const r={dates:['02-29','03-01'],years:{2026:[12,5],2024:[12,5]},median:[10,10]};
test('map preserves zero, missing, near-zero reference, and non-leap gaps',()=>{
 assert.equal(reading(r,2026,0).value,null);assert.equal(reading(r,2024,0).value,12);
 assert.equal(fillFor({value:null,median:10,percent:null},'inches').kind,'missing');
 assert.equal(fillFor({value:0,median:10,percent:0},'median').label,'Below 50%');
 assert.equal(fillFor({value:0,median:0,percent:null},'inches').label,'0');
 assert.equal(fillFor({value:1e-10,median:0,percent:null},'inches').label,'Under 1');
 assert.equal(fillFor({value:2,median:0,percent:null},'median').kind,'no-reference');
 assert.equal(displayReading({value:2,percent:null},'median'),'—');
});
test('automatic metric uses useful same-date references, explicit choice stays fixed',()=>{
 assert.equal(metricFor([r],2026,1,'auto'),'median');
 assert.equal(metricFor([{...r,median:[0,0]}],2026,1,'auto'),'inches');
 assert.equal(metricFor([r],2026,1,'inches'),'inches');
 assert.equal(fillFor({value:12,percent:120},'median').label,'120–149%');
});
test('geometry keeps all official basin identifiers with exactly eight linked series',()=>{
 const original=JSON.parse(fs.readFileSync('evidence/map/co_8.geojson'));
 const geometry=JSON.parse(fs.readFileSync('site/assets/colorado-basins.json'));
 assert.equal(geometry.basins.length,original.features.length);
 assert.equal(geometry.basins.filter(b=>b.id).length,8);
 assert.equal(new Set(geometry.basins.filter(b=>b.id).map(b=>b.id)).size,8);
 assert.deepEqual(geometry.basins.map(b=>b.source_id),original.features.map(f=>f.properties.id));
 assert(geometry.basins.every(b=>b.path.startsWith('M')&&b.path.endsWith('Z')));
 assert(!JSON.stringify(geometry).includes('NaN'));
});
