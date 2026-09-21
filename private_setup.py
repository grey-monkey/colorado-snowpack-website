"""One-use loopback form for secrets. No request bodies or credentials are logged."""
from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
from urllib.parse import parse_qs
import json
import secrets
import threading

root=Path(__file__).resolve().parent/'private'
root.mkdir(exist_ok=True)
nonce=secrets.token_urlsafe(32)

class Setup(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def do_GET(self):
        if self.path!='/':self.send_error(404);return
        body=f'''<!doctype html><html lang="en"><meta charset="utf-8"><title>Private Kit setup</title>
        <h1>Private Kit proof setup</h1><p>Saved only to this project’s ignored private folder. No production signup or sending.</p>
        <form method="post"><input type="hidden" name="nonce" value="{nonce}">
        <p><label>Kit test API key <input type="password" name="api_key" required autocomplete="off"></label></p>
        <p><label>Approved private test email <input type="email" name="email" required autocomplete="off"></label></p>
        <button>Save private test configuration</button></form></html>'''.encode()
        self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Content-Security-Policy',"default-src 'none'; form-action 'self'; frame-ancestors 'none'");self.end_headers();self.wfile.write(body)
    def do_POST(self):
        if self.headers.get('Origin')!='http://127.0.0.1:8766' or self.path!='/':self.send_error(403);return
        length=int(self.headers.get('Content-Length','0'))
        if not 0<length<8192:self.send_error(400);return
        fields=parse_qs(self.rfile.read(length).decode())
        if fields.get('nonce')!=[nonce]:self.send_error(403);return
        key=fields.get('api_key',[''])[0];email=fields.get('email',[''])[0]
        if not key or '@' not in email:self.send_error(400);return
        (root/'kit-config.json').write_text(json.dumps(dict(api_key=key,test_email=email)),encoding='utf-8')
        self.send_response(200);self.send_header('Content-Type','text/plain');self.send_header('Cache-Control','no-store');self.end_headers()
        self.wfile.write(b'Private configuration saved. No messages sent. You can close this tab.')
        threading.Thread(target=self.server.shutdown,daemon=True).start()

if __name__=='__main__':
    server=HTTPServer(('127.0.0.1',8766),Setup)
    print('One-use private setup: http://127.0.0.1:8766',flush=True)
    server.serve_forever();server.server_close()
