"""Hosted runner entry. Sending requires both workflow and backend switches."""
import json,os
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
from pipeline.refresh import connect,read_release,encoded
from pipeline.newsletter import edition

def main():
    db=connect(Path(os.environ.get('SNOWPACK_STORE','state/snowpack.sqlite')))
    try:release=read_release(db)
    finally:db.close()
    e=edition(release)
    if os.environ.get('WEEKLY_ENABLED')!='true':
        print(encoded({'edition':e['key'],'status':'generated_only'}));return
    base=os.environ['SIGNUP_SERVICE_URL'].rstrip('/')
    if not base.startswith('https://'):raise SystemExit('HTTPS backend required')
    request=Request(base+'/internal/weekly',data=encoded(e).encode(),headers={'Authorization':'Bearer '+os.environ['AUTOMATION_SECRET'],'Content-Type':'application/json'})
    try:
        with urlopen(request,timeout=35) as response:result=json.load(response)
    except (HTTPError,URLError,TimeoutError):raise SystemExit('Delivery not confirmed. Inspect the durable reservation and Kit; do not blindly resend.') from None
    print(encoded({k:result.get(k) for k in ('edition','broadcast_id','status')}))
if __name__=='__main__':main()
