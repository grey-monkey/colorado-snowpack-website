"""One refresh attempt plus last-good publication, with a truthful exit status."""
import argparse,os
from pathlib import Path
from .refresh import refresh,encoded
from .publish import publish

def run(store,output,signup_config=None):
    result=refresh(store)
    try:result['publication']=publish(store,output,signup_config=signup_config)
    except ValueError:result['publication']='No accepted data; output untouched'
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--store',type=Path,default=Path('state/snowpack.sqlite'));p.add_argument('--output',type=Path,default=Path('dist'));a=p.parse_args()
    config=None
    if os.environ.get('SIGNUP_ENABLED')=='true':
        endpoint=os.environ.get('SIGNUP_SERVICE_URL','').rstrip('/')
        if not endpoint.startswith('https://'):raise SystemExit('HTTPS signup service required')
        config={'enabled':True,'endpoint':endpoint+'/api/signup'}
    result=run(a.store,a.output,signup_config=config);print(encoded(result))
    raise SystemExit(0 if result['status'] in ('accepted','unchanged') else 1)
