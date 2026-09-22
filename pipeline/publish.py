"""Stage immutable release data, then atomically switch the public HTML entry."""
import argparse
import csv
import json
import os
import shutil
import tempfile
from datetime import date,timedelta
from pathlib import Path
from .build import ROOT
from .pages import render_pages
from .refresh import connect,read_release,encoded
from .weekly import facts
from .signup import configure


def atomic_text(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_name(path.name+'.next')
    temporary.write_text(value,encoding='utf-8')
    os.replace(temporary,path)


def snapshot_for(release):
    regions=[]
    newest=date.fromisoformat(release['observation_date']);year=newest.year+(newest.month>=10)
    dates=[(date(2015,10,1)+timedelta(days=i)).strftime('%m-%d') for i in range(366)]
    rows={(r['region_id'],r['water_year'],r['observation_date'][5:]):r for r in release['observations']}
    for p in release['metadata']['products']:
        # Reference from latest water year; Feb 29 requires a leap-year record.
        median=[]
        for md in dates:
            row=rows.get((p['region_id'],year,md))
            if row is None:
                row=next((rows[(p['region_id'],y,md)] for y in range(year-1,year-5,-1) if (p['region_id'],y,md) in rows),None)
            median.append(row['median_inches'] if row else None)
        years={str(y):[rows.get((p['region_id'],y,md),{}).get('swe_inches') for md in dates] for y in range(year-3,year+1)}
        regions.append(dict(id=p['region_id'],name=p['region_name'],source=p['source_chart'],
            coverage=[int(p['historical_water_years'][0]),year],station_labels=p['chart_series_labels'],
            dates=dates,median=median,years=years))
    return dict(schema_version='1.0.0',status='accepted',release_id=release['id'],observation_date=release['observation_date'],
        verified_at=release['accepted_at'],reference_period='1991–2020',units='inches SWE',method='accepted-v1',regions=regions)


def publish(store,output,signup_config=None):
    db=connect(store)
    try:
        release=read_release(db)
        attempt=db.execute('SELECT checked_at,status,reason FROM attempts ORDER BY id DESC LIMIT 1').fetchone()
    finally:db.close()
    output=Path(output)
    if release is None:
        raise ValueError('No accepted release; existing public build is untouched')
    rid=str(release['id']);data_relative='data/releases/'+rid
    output.mkdir(parents=True,exist_ok=True)
    # All generated outputs derive from this one database read, not a moving head.
    with tempfile.TemporaryDirectory(dir=output.parent,prefix='snowpack-stage-') as temp:
        stage=Path(temp)
        shutil.copytree(ROOT/'site',stage,dirs_exist_ok=True)
        render_pages(stage)
        configure(stage,signup_config)
        data=stage/'data';data.mkdir()
        snapshot=snapshot_for(release)
        metadata=dict(release['metadata'],release_id=release['id'],observation_date=release['observation_date'],
            accepted_at=release['accepted_at'],csv_null='Empty means unavailable; 0 means measured zero')
        (data/'snapshot.json').write_text(encoded(snapshot),encoding='utf-8')
        (data/'metadata.json').write_text(encoded(metadata),encoding='utf-8')
        (data/'series.json').write_text(encoded(dict(metadata=metadata,observations=release['observations'])),encoding='utf-8')
        with (data/'series.csv').open('w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=list(release['observations'][0]));writer.writeheader();writer.writerows(release['observations'])
        # Facts are versioned with accepted data; age eligibility is evaluated at send time.
        recap=facts(release,today=date.fromisoformat(release['observation_date']))
        recap.pop('delivery_eligible')
        (data/'weekly.json').write_text(encoded(recap),encoding='utf-8')
        target=output/data_relative;target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists():
            # Same-volume rename of a complete directory. Interrupted stages do
            # not obstruct a later recovery attempt or affect the current entry.
            pending=Path(tempfile.mkdtemp(dir=target.parent,prefix='.stage-'))
            shutil.copytree(data,pending,dirs_exist_ok=True)
            os.replace(pending,target)
        # Publish local fonts and photographs as bytes before the HTML references them.
        for asset in (stage/'assets').rglob('*') if (stage/'assets').exists() else []:
            if asset.is_file():
                destination=output/asset.relative_to(stage)
                destination.parent.mkdir(parents=True,exist_ok=True)
                pending_asset=destination.with_name(destination.name+'.next')
                shutil.copyfile(asset,pending_asset)
                os.replace(pending_asset,destination)
        for file in stage.iterdir():
            if not file.is_file() or file.name=='index.html':continue
            content=file.read_text(encoding='utf-8')
            if file.suffix=='.html':
                content=accepted_page(content,release,data_relative)
            atomic_text(output/file.name,content)
        health=dict(checked_at=attempt[0],status=attempt[1],release_id=release['id'])
        atomic_text(output/'data/health.json',encoded(health))
        index=(stage/'index.html').read_text(encoding='utf-8')
        index=index.replace('<body>',f'<body data-snapshot="{data_relative}/snapshot.json" data-health="data/health.json">')
        index=accepted_page(index,release,data_relative)
        # Last operation: the entry references a complete immutable data directory.
        atomic_text(output/'index.html',index)
    return dict(release_id=release['id'],observation_date=release['observation_date'],update_status=attempt[1],output=str(output))


def accepted_page(content,release,data_relative):
    observed=date.fromisoformat(release['observation_date'])
    year=observed.year+(observed.month>=10)
    content=content.replace('water years 2024–2026',f'water years {year-2}–{year}')
    content=content.replace('water years 1987–2026',f'water years 1987–{year}').replace('water years 1986–2026',f'water years 1986–{year}')
    content=content.replace('data/series.',data_relative+'/series.').replace('data/metadata.json',data_relative+'/metadata.json')
    content=content.replace('Frozen research snapshot · September 21, 2026.',f'Accepted observations · {release["observation_date"]}.')
    content=content.replace('This local preview does not retrieve new measurements automatically.','This local preview uses validated retrieved data. No production refresh schedule is active.')
    content=content.replace('30,378 annual/reference value positions',f'{sum(p["matched_values"] for p in release["metadata"]["products"]):,} annual/reference value positions')
    content=content.replace('The frozen preview retains the original values; it is not silently refreshed.','Accepted revisions are retained in a versioned history; each download identifies its accepted release.')
    content=content.replace('This is a frozen local preview; production revisions will need dated correction records.','This is a local accepted-data preview. Revision history is retained; a public correction browser is not included.')
    content=content.replace('Exports retain schema <code>0.1.0</code> and method <code>nrcs-published-por-v1</code>.','Exports retain schema <code>0.1.0</code> and use method <code>accepted-v1</code>.')
    return content


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--store',type=Path,default=Path('state/snowpack.sqlite'));p.add_argument('--output',type=Path,default=ROOT/'dist')
    a=p.parse_args();print(encoded(publish(a.store,a.output)))
