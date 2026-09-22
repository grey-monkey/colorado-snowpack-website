"""Build a noindex, owner-only signup rehearsal from accepted data (no retrieval)."""
from pathlib import Path
from pipeline.publish import publish

def build():
    output=Path('worker-dist')
    publish(Path('state/snowpack.sqlite'),output,signup_config={'enabled':True,'endpoint':'/api/signup'})
    for page in output.glob('*.html'):
        s=page.read_text(encoding='utf-8').replace('</head>','<meta name="robots" content="noindex,nofollow"></head>')
        s=s.replace('<main id="main"','<aside class="notice" style="margin:1rem">Private readiness test. Signup accepts only the approved test address. No public launch or recurring sending.</aside><main id="main"',1)
        page.write_text(s,encoding='utf-8')
    (output/'robots.txt').write_text('User-agent: *\nDisallow: /\n')
if __name__=='__main__':build()
