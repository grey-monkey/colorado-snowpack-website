"""One refresh attempt plus last-good publication, with a truthful exit status."""
import argparse
from pathlib import Path
from .refresh import refresh,encoded
from .publish import publish

def run(store,output):
    result=refresh(store)
    try:result['publication']=publish(store,output)
    except ValueError:result['publication']='No accepted data; output untouched'
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--store',type=Path,default=Path('state/snowpack.sqlite'));p.add_argument('--output',type=Path,default=Path('dist'));a=p.parse_args()
    result=run(a.store,a.output);print(encoded(result))
    raise SystemExit(0 if result['status'] in ('accepted','unchanged') else 1)
