"""Deterministic weekly email and fail-closed, owner-only Kit delivery proof."""
import argparse,hashlib,json,sqlite3
from datetime import date,datetime,timezone
from html import escape
from pathlib import Path
from urllib.request import Request,urlopen
from .refresh import connect,read_release,encoded
from .weekly import facts

from .proof import PRODUCTS

NAMES={rid: ('Colorado statewide' if rid=='co-state' else name) for rid,name,_ in PRODUCTS.values()}

def number(v):
    if v is None:return 'Unavailable'
    if 0<abs(v)<0.005:return ('−' if v<0 else '')+'<0.005'
    return f'{v:.2f}'

def edition(release,base_url='https://coloradosnowpack.com',today=None):
    if not base_url.startswith('https://'):raise ValueError('Email dashboard link must use HTTPS')
    f=facts(release,today=today)
    if not f['delivery_eligible']:raise ValueError('Withheld: stale data or missing weekly endpoint')
    iso=date.fromisoformat(f['end']).isocalendar()
    key=f'snowpack-weekly:{iso.year}-W{iso.week:02d}'
    rows=[];plain=[]
    for r in f['regions']:
        name=NAMES[r['region_id']];delta=r['net_swe_change_inches']
        pp=r['percentage_point_change']
        comparison='Percentage comparison omitted because the historical reference is near zero or unavailable.' if pp is None else f'{pp:+.1f} percentage points in percent of median.'
        summary=f'{number(r["end_swe_inches"])} inches SWE; net change {number(delta)} inches over seven days.'
        rows.append(f'<h2 style="font:700 21px Georgia,serif;color:#173e32;margin:28px 0 8px">{escape(name)}</h2><p>{escape(summary)}</p><p style="font-size:14px">{escape(comparison)}</p>')
        plain.append(name+'\n'+summary+'\n'+comparison)
    title='Colorado Snowpack Weekly · '+f['end']
    content=f'''<div style="max-width:600px;margin:0 auto;color:#23392f;font:16px/1.65 Arial,sans-serif"><p style="font-size:12px;letter-spacing:2px;color:#426454">COLORADO SNOWPACK WEEKLY</p><h1 style="font:normal 32px/1.15 Georgia,serif;color:#173e32">The week in snow.</h1><p><strong>{f['start']} to {f['end']}</strong></p><p>A seven-day view of water held in snow at NRCS monitoring sites.</p>{''.join(rows)}<p><a style="color:#173e32;font-weight:bold" href="{escape(base_url.rstrip('/')+'/',quote=True)}">Explore the snowpack →</a></p><p style="font-size:13px;color:#4b5c52">Source: USDA NRCS published station-based SWE series. Net change is not snowfall; changing station coverage can affect small changes. Measurements are provisional. Observed {f['end']}.</p><p style="font-size:13px"><a href="{escape(base_url.rstrip('/')+'/methods.html',quote=True)}">Sources and methods</a></p></div>'''
    text=title+'\n'+f['start']+' to '+f['end']+'\n\n'+'\n\n'.join(plain)+'\n\nNet SWE change is not snowfall. Source: USDA NRCS. Daily station coverage not independently verified.\n'+base_url
    return dict(key=key,subject=title,content=content,text=text,facts=f)

class Kit:
    def __init__(self,key):self.key=key
    def call(self,path,data=None):
        request=Request('https://api.kit.com/v4/'+path,data=encoded(data).encode() if data is not None else None,headers={'X-Kit-Api-Key':self.key,'Content-Type':'application/json'})
        with urlopen(request,timeout=30) as response:return json.load(response)


def send_private(e,config,ledger,client=None):
    """No production/all-subscriber mode. Each edition+test address can send once."""
    client=client or Kit(config['api_key'])
    target=config['test_email'].casefold();tag=int(config['tag_id'])
    members=client.call(f'tags/{tag}/subscribers')
    if members['pagination'].get('has_next_page') or len(members['subscribers'])!=1:
        raise ValueError('Private tag must contain exactly one active test recipient')
    member=members['subscribers'][0]
    if member['email_address'].casefold()!=target or member['state']!='active':
        raise ValueError('Approved test recipient is not active')
    key=e['key']+':private:'+hashlib.sha256(target.encode()).hexdigest()[:16]
    ledger=Path(ledger);ledger.parent.mkdir(parents=True,exist_ok=True)
    db=sqlite3.connect(ledger,timeout=30)
    db.execute('CREATE TABLE IF NOT EXISTS editions(edition TEXT PRIMARY KEY, state TEXT, broadcast_id INTEGER, content_hash TEXT, created_at TEXT)')
    try:
        db.execute('BEGIN IMMEDIATE')
        if db.execute('SELECT 1 FROM editions WHERE edition=?',(key,)).fetchone():raise ValueError('Edition already reserved; reconcile, never blindly resend')
        db.execute('INSERT INTO editions VALUES(?,?,?,?,?)',(key,'attempting',None,hashlib.sha256(e['content'].encode()).hexdigest(),datetime.now(timezone.utc).isoformat()));db.commit()
        payload={'email_template_id':int(config['template_id']),'subject':'[Private rehearsal] '+e['subject'],'description':key,'content':e['content'],'public':False,'send_at':datetime.now(timezone.utc).isoformat(),'subscriber_filter':[{'all':[{'type':'tag','ids':[tag]}]}]}
        # No retries: an interrupted response may still have created a broadcast.
        result=client.call('broadcasts',payload)['broadcast']
        db.execute('UPDATE editions SET state=?,broadcast_id=? WHERE edition=?',(result['status'],result['id'],key));db.commit()
        return {'edition':e['key'],'broadcast_id':result['id'],'status':result['status'],'public':result['public']}
    finally:db.close()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--store',type=Path,default=Path('state/snowpack.sqlite'));p.add_argument('--output',type=Path,default=Path('work/edition'));p.add_argument('--base-url',default='https://coloradosnowpack.com');p.add_argument('--private-send-config',type=Path);p.add_argument('--ledger',type=Path,default=Path('private/editions.sqlite'));a=p.parse_args()
    db=connect(a.store)
    try:r=read_release(db)
    finally:db.close()
    if r is None:raise SystemExit('No accepted history')
    e=edition(r,base_url=a.base_url);a.output.mkdir(parents=True,exist_ok=True)
    (a.output/'email.html').write_text(e['content'],encoding='utf-8');(a.output/'email.txt').write_text(e['text'],encoding='utf-8');(a.output/'edition.json').write_text(encoded(e),encoding='utf-8')
    if a.private_send_config:print(encoded(send_private(e,json.loads(a.private_send_config.read_text()),a.ledger)))
    else:print(encoded({'edition':e['key'],'status':'generated_only','release_id':r['id']}))
