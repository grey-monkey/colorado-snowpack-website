"""Bounded retrieval, existing NRCS proof, and transactional accepted history."""
import argparse
import hashlib
import json
import re
import sqlite3
import time
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo
from .proof import BASE, PRODUCTS, verify

VERSION='accepted-v1'
MAX_BYTES=4_000_000


def encoded(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)


def digest(value):
    return hashlib.sha256(value).hexdigest()


def connect(path):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    db=sqlite3.connect(path,timeout=30)
    db.execute('PRAGMA foreign_keys=ON')
    db.executescript('''
      CREATE TABLE IF NOT EXISTS releases(id INTEGER PRIMARY KEY, fingerprint TEXT UNIQUE,
        observation_date TEXT NOT NULL, accepted_at TEXT NOT NULL, metadata TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS revisions(region TEXT NOT NULL, day TEXT NOT NULL,
        release_id INTEGER NOT NULL REFERENCES releases(id), value TEXT NOT NULL,
        PRIMARY KEY(region,day,release_id));
      CREATE TABLE IF NOT EXISTS attempts(id INTEGER PRIMARY KEY, checked_at TEXT,
        status TEXT, reason TEXT, release_id INTEGER REFERENCES releases(id));
    ''')
    return db


def read_release(db, release_id=None):
    release=db.execute('SELECT id,observation_date,accepted_at,metadata FROM releases '+
        ('WHERE id=?' if release_id is not None else 'ORDER BY id DESC LIMIT 1'),
        (release_id,) if release_id is not None else ()).fetchone()
    if release is None:
        return None
    rows=db.execute('''SELECT r.value FROM revisions r JOIN
        (SELECT region,day,MAX(release_id) AS version FROM revisions WHERE release_id<=?
         GROUP BY region,day) latest
        ON r.region=latest.region AND r.day=latest.day AND r.release_id=latest.version
        ORDER BY r.region,r.day''',(release[0],)).fetchall()
    return dict(id=release[0],observation_date=release[1],accepted_at=release[2],
        metadata=json.loads(release[3]),observations=[json.loads(r[0]) for r in rows])


class Rejected(ValueError):
    def __init__(self,status,reason):
        self.status=status;self.reason=reason
        super().__init__(reason)


def retrieve(url):
    # Fixed official HTTPS URLs only; prevent redirected credential/host surprises.
    last=None
    for attempt in range(3):
        try:
            with urlopen(Request(url,headers={'User-Agent':'ColoradoSnowpack/1.0 (public NRCS data verification)'}),timeout=25) as response:
                if not response.url.startswith(BASE):
                    raise Rejected('retrieval_failed','unexpected_redirect')
                data=response.read(MAX_BYTES+1)
                if len(data)>MAX_BYTES:
                    raise Rejected('retrieval_failed','source_size_limit')
                return data
        except Rejected:
            raise
        except (OSError,TimeoutError) as error:
            last=error
            if attempt<2:time.sleep(2**attempt)
    raise Rejected('retrieval_failed','upstream_unavailable') from last


def candidate(payloads,today):
    observations=[];proofs=[];hashes={};dates=[]
    current_year=today.year+(today.month>=10)
    for key in PRODUCTS:
        raw=payloads[key+'.json'];html=payloads[key+'-chart.html']
        hashes[key+'.json']=digest(raw);hashes[key+'-chart.html']=digest(html)
        rows=json.loads(raw);text=html.decode('utf-8')
        normalized,proof=verify(rows,text,key)
        # The daily source must describe this water year, not a cached old season.
        if max(map(int,proof['historical_water_years']))!=current_year:
            raise Rejected('source_missing','current_water_year_unavailable')
        reported=[]
        for annotation in proof['chart_status']:
            match=re.search(r'Current as of (\d{2}/\d{2}/\d{4})',annotation)
            if match:reported.append(datetime.strptime(match[1],'%m/%d/%Y').date())
        if len(set(reported))!=1:
            raise Rejected('validation_failed','ambiguous_source_date')
        observed=date.fromisoformat(proof['latest']['observation_date'])
        if observed!=reported[0]:
            raise Rejected('source_missing','latest_observation_missing')
        if observed>today or (today-observed).days>2:
            raise Rejected('source_missing','source_date_outside_freshness_window')
        for row in normalized:
            if row['observation_date']>observed.isoformat() and row['swe_inches'] is not None:
                raise Rejected('validation_failed','future_observation')
        dates.append(observed)
        observations.extend(normalized);proofs.append(proof)
    if len(set(dates))!=1:
        raise Rejected('source_missing','products_not_aligned')
    # Do not store placeholder future dates as historical observations.
    observations=[r for r in observations if r['observation_date']<=dates[0].isoformat()]
    observations.sort(key=lambda r:(r['region_id'],r['observation_date']))
    return dict(observation_date=dates[0].isoformat(),observations=observations,
        metadata=dict(schema_version='0.1.0',method_version=VERSION,source_sha256=hashes,
            products=proofs,status='accepted',reference_period='1991-2020',units='inches SWE',
            limitation='Published station-based series; daily coverage and weights not independently verified.'))


def refresh(path,fetch=retrieve,now=None):
    now=now or datetime.now(timezone.utc)
    today=now.astimezone(ZoneInfo('America/Denver')).date()
    checked=now.isoformat()
    db=connect(path)
    try:
        payloads={}
        for key,(_,_,product) in PRODUCTS.items():
            for extension,suffix in [('json','.json'),('html','-chart.html')]:
                payloads[key+suffix]=fetch(BASE+product+'.'+extension)
        try:
            incoming=candidate(payloads,today)
        except Rejected:
            raise
        except (ValueError,KeyError,IndexError,TypeError,UnicodeError) as e:
            raise Rejected('validation_failed','source_proof_rejected') from e
        # Content identity excludes retrieval timestamps and raw chart rendering IDs.
        fingerprint=digest(encoded([incoming['observations'],incoming['metadata']['products']]).encode())
        db.execute('BEGIN IMMEDIATE')
        previous=read_release(db)
        if previous and incoming['observation_date']<previous['observation_date']:
            raise Rejected('validation_failed','observation_date_regression')
        existing=db.execute('SELECT id FROM releases WHERE fingerprint=?',(fingerprint,)).fetchone()
        if existing:
            if not previous or existing[0]!=previous['id']:
                raise Rejected('validation_failed','old_release_replay')
            rid=existing[0];state='unchanged';changes=0
        else:
            old={(r['region_id'],r['observation_date']):encoded(r) for r in previous['observations']} if previous else {}
            incoming_keys={(r['region_id'],r['observation_date']) for r in incoming['observations']}
            if old.keys()-incoming_keys:
                raise Rejected('validation_failed','historical_coverage_removed')
            lost=sum(1 for r in incoming['observations'] if r['swe_inches'] is None and
                (r['region_id'],r['observation_date']) in old and json.loads(old[(r['region_id'],r['observation_date'])])['swe_inches'] is not None)
            if lost>max(10,len(old)*0.01):
                raise Rejected('validation_failed','excessive_new_missing_values')
            rid=db.execute('INSERT INTO releases(fingerprint,observation_date,accepted_at,metadata) VALUES(?,?,?,?)',
                (fingerprint,incoming['observation_date'],checked,encoded(incoming['metadata']))).lastrowid
            changes=0
            for r in incoming['observations']:
                value=encoded(r);key=(r['region_id'],r['observation_date'])
                if old.get(key)!=value:
                    db.execute('INSERT INTO revisions VALUES(?,?,?,?)',(*key,rid,value));changes+=1
            state='accepted'
        db.execute('INSERT INTO attempts(checked_at,status,reason,release_id) VALUES(?,?,?,?)',(checked,state,None,rid))
        db.commit()
        return dict(status=state,release_id=rid,changed_observations=changes,observation_date=incoming['observation_date'])
    except (Rejected,OSError,TimeoutError) as error:
        db.rollback()
        status=error.status if isinstance(error,Rejected) else 'retrieval_failed'
        reason=error.reason if isinstance(error,Rejected) else 'upstream_unavailable'
        current=read_release(db)
        db.execute('INSERT INTO attempts(checked_at,status,reason,release_id) VALUES(?,?,?,?)',
            (checked,status,reason,current['id'] if current else None));db.commit()
        return dict(status=status,reason=reason,retained_release=current['id'] if current else None)
    finally:
        db.close()


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--store',type=Path,default=Path('state/snowpack.sqlite'))
    args=parser.parse_args()
    result=refresh(args.store)
    print(encoded(result))
    raise SystemExit(0 if result['status'] in ('accepted','unchanged') else 1)
