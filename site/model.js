// Pure presentation rules shared by the browser and Node tests.
export function calendarDate(year, md) {
  const [m,d]=md.split('-').map(Number), y=m>=10?year-1:year;
  const result=new Date(Date.UTC(y,m-1,d));
  return result.getUTCMonth()===m-1 && result.getUTCDate()===d ? result.toISOString().slice(0,10) : null;
}
export function ratio(value, median) {
  return value===null || median===null || median<0.1 ? null : value/median*100;
}
export function condition(value, median) {
  if(value===null) return {kind:'missing', headline:'Observation unavailable', text:'There is no reported value for this date. Missing data does not mean no snow.'};
  if(median===null) return {kind:'reference-missing', headline:'The comparison is unavailable', text:'A snow-water value is available, but its same-date historical reference is missing.'};
  if(median<0.1) return {kind:'low-reference', headline:'A quiet point in the snow season.', text:median===0?'The historical median is zero on this date, so a percentage comparison would be misleading. Follow the season below for context.':'The historical median is near zero on this date, so a percentage comparison would exaggerate small differences.'};
  const percent=ratio(value,median);
  return {kind:'normal', headline:`${Math.round(percent)}% of the same-date median.`, text:'A comparison with the published 1991–2020 reference for this date. This describes water held in snow at monitoring sites.'};
}
export function freshness(snapshot, now=new Date()) {
  const parts=Object.fromEntries(new Intl.DateTimeFormat('en-US',{timeZone:'America/Denver',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(now).map(p=>[p.type,p.value]));
  const age=Math.floor((Date.UTC(Number(parts.year),Number(parts.month)-1,Number(parts.day))-Date.parse(snapshot.observation_date+'T00:00:00Z'))/86400000);
  return {stale:age>2, age, label:snapshot.status==='frozen'?'Frozen snapshot · not updating':age>2?'Older data · update overdue':'Latest available snapshot'};
}
export function yearSeries(region, year) {
  return region.dates.map((md,i)=>({md,date:calendarDate(year,md),value:calendarDate(year,md)?region.years[year]?.[i]??null:null,median:region.median[i]}));
}
export function weeklyChange(region, date) {
  const end=new Date(date+'T00:00:00Z'), start=new Date(end.getTime()-7*86400000);
  const valueAt=d=> {const year=d.getUTCFullYear()+(d.getUTCMonth()>=9?1:0); return region.years[year]?.[region.dates.indexOf(d.toISOString().slice(5,10))]??null;};
  const a=valueAt(start), b=valueAt(end);
  return {start:start.toISOString().slice(0,10),end:date,value:a===null||b===null?null:b-a};
}
export function validateSnapshot(s) {
  if(s.schema_version!=='1.0.0'||!['frozen','accepted'].includes(s.status)||!/^\d{4}-\d{2}-\d{2}$/.test(s.observation_date)||!Array.isArray(s.regions)||!s.regions.length) throw new Error('Unsupported snapshot');
  for(const r of s.regions) {
    if(!r.id||!r.name||r.dates?.length!==366||new Set(r.dates).size!==366||r.median?.length!==366||!Object.keys(r.years||{}).length) throw new Error('Incomplete region');
    for(const values of [r.median,...Object.values(r.years)]) {
      if(values.length!==366||values.some(v=>v!==null&&(typeof v!=='number'||!Number.isFinite(v)||v<0))) throw new Error('Invalid observations');
    }
  }
  return s;
}
