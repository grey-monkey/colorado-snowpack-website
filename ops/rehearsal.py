"""Clean hosted rehearsal: restore public accepted history, refresh and stage preview."""
import gzip,json,sqlite3
from pathlib import Path
from pipeline.run import run

def main():
    state=Path('state');state.mkdir(exist_ok=True)
    db=state/'snowpack.sqlite'
    if not db.exists():db.write_bytes(gzip.decompress(Path('evidence/accepted-history.sqlite.gz').read_bytes()))
    con=sqlite3.connect(db)
    try:assert con.execute('PRAGMA quick_check').fetchone()[0]=='ok'
    finally:con.close()
    result=run(db,Path('preview-dist'))
    assert (Path('preview-dist')/'index.html').exists()
    for page in Path('preview-dist').glob('*.html'):
        s=page.read_text(encoding='utf-8').replace('</head>','<meta name="robots" content="noindex,nofollow"></head>')
        s=s.replace('<body','<body',1).replace('<main id="main"','<aside class="notice" style="margin:1rem">Temporary readiness preview. Public subscriptions and recurring jobs are inactive.</aside><main id="main"',1)
        assert 'data-sv-form=' not in s
        page.write_text(s,encoding='utf-8')
    Path('preview-dist/robots.txt').write_text('User-agent: *\nDisallow: /\n')
    Path('preview-dist/.nojekyll').touch()
    Path('preview-dist/rehearsal.json').write_text(json.dumps({'status':result['status'],'release_id':result.get('release_id',result.get('retained_release')),'signup_enabled':False,'schedule_enabled':False}))
    print(json.dumps(result))
if __name__=='__main__':main()
