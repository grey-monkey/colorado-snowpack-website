import {calendarDate,condition,freshness,yearSeries,weeklyChange,validateSnapshot} from './model.js';
const $=id=>document.getElementById(id);
const fmtDate=s=>new Date(s+'T12:00:00Z').toLocaleDateString('en-US',{month:'long',day:'numeric',year:'numeric',timeZone:'UTC'});
const fmt=v=>v===null?'Not reported':v===0?'0.00':v<0.005?'<0.005':v.toFixed(2);
let snapshot, region, year, current, previous;
function renderChart(){
  const width=Math.max(280,$('chart').clientWidth), height=width<600?235:290,left=36,right=14,top=10,bottom=29;
  const max=Math.max(1,...current.map(x=>x.value??0),...previous.map(x=>x.value??0),...region.median.map(x=>x??0));
  const step=Math.max(1,Math.ceil(max/4)), ymax=step*4;
  const x=i=>left+i/365*(width-left-right), y=v=>height-bottom-v/ymax*(height-top-bottom);
  const path=values=>{let drawing=false;return values.map((v,i)=>{if(v===null){drawing=false;return '';}const s=`${drawing?'L':'M'}${x(i).toFixed(2)},${y(v).toFixed(2)}`;drawing=true;return s;}).join(' ');};
  let svg=`<svg viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="chart-title chart-desc"><title id="chart-title">${region.name} snow water equivalent, water years ${year} and ${year-1}</title><desc id="chart-desc">Daily values in inches, compared with the published 1991–2020 median. Missing values are gaps. Use the date slider or numerical table for exact values.</desc>`;
  for(let n=0;n<=4;n++)svg+=`<line x1="${left}" y1="${y(n*step)}" x2="${width-right}" y2="${y(n*step)}" stroke="#dce3da"/><text x="${left-10}" y="${y(n*step)+4}" text-anchor="end">${n*step}</text>`;
  const months=width<500?['10','12','02','04','06','08']:['10','11','12','01','02','03','04','05','06','07','08','09'];
  for(const m of months){const i=region.dates.indexOf(m+'-01');svg+=`<text x="${x(i)}" y="${height-7}" text-anchor="middle">${new Date('2000-'+m+'-01T12:00:00Z').toLocaleString('en-US',{month:'short',timeZone:'UTC'})}</text>`;}
  svg+=`<path d="${path(region.median)}" fill="none" stroke="#7b8c7d" stroke-width="2" stroke-dasharray="2 5"/><path d="${path(previous.map(r=>r.value))}" fill="none" stroke="#a95328" stroke-width="2" stroke-dasharray="7 5"/><path d="${path(current.map(r=>r.value))}" fill="none" stroke="#1b6355" stroke-width="3"/>`;
  const index=Number($('day').value);svg+=`<line x1="${x(index)}" x2="${x(index)}" y1="${top}" y2="${height-bottom}" stroke="#526862" stroke-dasharray="2 4"/>`;
  if(current[index].value!==null)svg+=`<circle cx="${x(index)}" cy="${y(current[index].value)}" r="4" fill="#1b6355" stroke="#fff" stroke-width="2"/>`;
  $('chart').innerHTML=svg+'</svg>';
}
function inspectDate(){
  const i=Number($('day').value), row=current[i], prev=previous[i];
  const title=row.date?fmtDate(row.date):`February 29 · no calendar date in water year ${year}`;
  $('date-reading').replaceChildren();
  const strong=document.createElement('strong');strong.textContent=title;$('date-reading').append(strong);
  for(const [label,value] of [[year,row.value],[year-1,prev.value],['Historic Median',row.median]]){const div=document.createElement('div'),b=document.createElement('b'),span=document.createElement('span');b.textContent=value===null?'—':fmt(value)+' in';span.textContent=label+(value===null?' · not reported':'');div.append(b,span);$('date-reading').append(div);}
  $('day').setAttribute('aria-valuetext',`${title}; ${year}: ${fmt(row.value)} inches; ${year-1}: ${fmt(prev.value)} inches; historic median: ${fmt(row.median)} inches`);
  renderChart();
}
function renderSeason(){
  current=yearSeries(region,year);previous=yearSeries(region,year-1);
  $('current-legend').textContent=year;$('previous-legend').textContent=year-1;
  $('table-current').textContent=year+' · in';$('table-previous').textContent=year-1+' · in';
  $('table-caption').textContent=`${region.name}. Water years ${year} and ${year-1}, aligned by month and day. SWE in inches. Median: 1991–2020. “Not reported” is different from zero.`;
  $('table-body').replaceChildren();
  for(let i=0;i<366;i++){const tr=document.createElement('tr');const values=[region.dates[i],current[i].date?fmt(current[i].value):'No leap date',previous[i].date?fmt(previous[i].value):'No leap date',fmt(region.median[i])];for(const [j,v]of values.entries()){const td=document.createElement(j===0?'th':'td');if(j===0)td.scope='row';td.textContent=v;tr.append(td);}$('table-body').append(tr);}
  const latestYear=Number(snapshot.observation_date.slice(0,4))+(Number(snapshot.observation_date.slice(5,7))>=10?1:0);
  $('chart-note').textContent=`${year===latestYear?'The latest season ends at the last reported observation. ':''}Gaps mean no reported value; years align by month and day. The mix of reporting stations can change. NRCS may revise these readings.`;
  inspectDate();
}
function renderRegion(){
  const date=snapshot.observation_date, waterYear=Number(date.slice(0,4))+(Number(date.slice(5,7))>=10?1:0), i=region.dates.indexOf(date.slice(5,10));
  const value=region.years[waterYear]?.[i]??null,median=region.median[i]??null,state=condition(value,median);
  $('condition-title').textContent=state.headline;$('condition-copy').textContent=state.text;
  $('swe').textContent=value===null?'—':fmt(value);$('median').textContent=median===null?'Not reported':fmt(median)+' inches';
  $('reading-label').textContent=value===null?'No reported observation for this date':'Snow water at NRCS monitoring sites';
  $('observation').textContent=`${region.id==='co-state'?'STATEWIDE':region.name.toUpperCase()} · ${fmtDate(date)}`;
  $('source').href=region.source;
  const change=weeklyChange(region,date);$('week-range').textContent=`${fmtDate(change.start)} – ${fmtDate(change.end)}`;
  $('change-title').textContent=change.value===null?'A weekly comparison is unavailable.':Math.abs(change.value)<0.005?'Little change over the past week.':`${Math.abs(change.value).toFixed(2)} inches ${change.value<0?'less':'more'} than a week earlier.`;
  $('change-copy').textContent=change.value===null?'A measurement is missing for one of the two dates, so we cannot calculate the weekly change.':'This compares the water held in snow now with a week ago. It is not a snowfall total. The reporting sites can change from day to day, so small differences deserve some caution.';
  renderSeason();
}
function syncURL(){const u=new URL(location.href);u.searchParams.set('region',region.id);u.searchParams.set('year',year);history.replaceState(null,'',u);}
async function load(){
  $('load-error').hidden=true;$('dashboard').hidden=true;$('snapshot-status').textContent='Loading the verified snowpack snapshot…';
  try{
    const response=await fetch(document.body.dataset.snapshot||'data/snapshot.json',{signal:AbortSignal.timeout(10000)});if(!response.ok)throw new Error('Snapshot unavailable');snapshot=validateSnapshot(await response.json());
    const params=new URLSearchParams(location.search);region=snapshot.regions.find(r=>r.id===params.get('region'))||snapshot.regions[0];
    const allYears=Object.keys(region.years).map(Number).sort((a,b)=>b-a);const years=allYears.filter(y=>allYears.includes(y-1));year=years.includes(Number(params.get('year')))?Number(params.get('year')):years[0];
    const groups=new Map();
    for(const r of snapshot.regions){
      const label=r.group||(r.id==='co-state'?'Statewide':'River basins');
      if(!groups.has(label)){const group=document.createElement('optgroup');group.label=label;groups.set(label,group);}
      groups.get(label).append(new Option(r.id==='co-state'?'Colorado statewide':r.name,r.id));
    }
    $('region').replaceChildren(...groups.values());$('region').value=region.id;
    $('season').replaceChildren(...years.map(y=>new Option(y,y)));$('season').value=year;
    $('day').value=Math.max(0,region.dates.indexOf(snapshot.observation_date.slice(5,10)));
    const status=freshness(snapshot);$('snapshot-status').textContent=`${status.label} · Observed ${fmtDate(snapshot.observation_date)}${status.stale?' · '+status.age+' days old':''}`;
    $('dashboard').hidden=false;renderRegion();
    if(document.body.dataset.health){
      // Health failure must never hide an already accepted data snapshot.
      try{const healthResponse=await fetch(document.body.dataset.health,{cache:'no-store',signal:AbortSignal.timeout(4000)});
        if(healthResponse.ok){const health=await healthResponse.json();if(!['accepted','unchanged'].includes(health.status))$('snapshot-status').textContent+=' · The latest update could not be completed. Showing the last verified readings.';}
      }catch{/* The age label remains reliable even when the health file cannot load. */}
    }
  }catch(error){$('snapshot-status').textContent='Snapshot unavailable · no measurements displayed';$('load-error').hidden=false;}
}
$('region').addEventListener('change',()=>{region=snapshot.regions.find(r=>r.id===$('region').value);renderRegion();syncURL();});
$('season').addEventListener('change',()=>{year=Number($('season').value);renderSeason();syncURL();});
$('day').addEventListener('input',inspectDate);$('retry').addEventListener('click',load);
new ResizeObserver(()=>{if(current)renderChart();}).observe($('chart'));
load();
