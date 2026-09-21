"""Serve only the built public directory on loopback; never the source or home."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from pathlib import Path
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=8765)
args=parser.parse_args()
root=Path(__file__).resolve().parent/'dist'
if not (root/'index.html').is_file():
    raise SystemExit('First run: python -m pipeline.build')
server=ThreadingHTTPServer(('127.0.0.1',args.port),partial(SimpleHTTPRequestHandler,directory=str(root)))
print(f'Local preview: http://127.0.0.1:{args.port}',flush=True)
server.serve_forever()
