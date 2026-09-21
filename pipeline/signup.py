"""Public signup markup. Configuration contains public form IDs only, never keys."""
from html import escape
import json
from pathlib import Path

SUCCESS='Check your inbox to confirm your subscription. Already confirmed? You are all set. If nothing arrives, check spam or try again later.'

def markup(config=None):
    if not config or not config.get('enabled'):
        return '<div class="signup-box"><p class="pill">Opening soon</p><p>A concise weekly recap of Colorado snowpack conditions and meaningful changes.</p><p>Subscriptions are not open yet.</p><a href="weekly.html">About the weekly →</a></div>'
    form=str(config['form_id']);uid=str(config['uid'])
    if not form.isdigit() or not uid.isalnum():raise ValueError('Invalid public form configuration')
    options={'settings':{'after_subscribe':{'action':'message','success_message':SUCCESS,'redirect_url':''},'analytics':{},'recaptcha':{'enabled':True},'return_visitor':{'action':'show','custom_content':''},'powered_by':{'show':True,'url':'https://kit.com/features/forms'}},'version':'5'}
    return f'''<div class="signup-box" data-signup>
<form action="https://app.kit.com/forms/{form}/subscriptions" method="post" class="seva-form formkit-form" data-sv-form="{form}" data-uid="{uid}" data-format="inline" data-version="5" data-options="{escape(json.dumps(options),quote=True)}">
<ul class="formkit-alert formkit-alert-error" data-element="errors" data-group="alert" role="alert"></ul>
<div data-element="fields" class="formkit-fields"><div class="formkit-field"><label for="signup-email">Email address</label><input id="signup-email" class="formkit-input" name="email_address" type="email" required autocomplete="email" inputmode="email" aria-describedby="signup-consent"></div>
<button data-element="submit" class="formkit-submit" type="submit" disabled><span>Join the weekly</span></button></div>
<p id="signup-consent" class="small">By subscribing, you agree to receive Colorado Snowpack Weekly. Confirm by email to join. Unsubscribe at any time. <a href="privacy.html">Privacy</a>.</p>
<a href="https://kit.com/features/forms" data-element="powered-by" rel="noopener" class="small">Built with Kit</a>
</form><p class="signup-status small" role="status" aria-live="polite">Loading the signup form…</p><noscript><p>Please enable JavaScript to use the protected signup form.</p></noscript></div>'''

def configure(output,config=None):
    output=Path(output)
    for name in ('index.html','weekly.html'):
        p=output/name;s=p.read_text(encoding='utf-8')
        s=s.replace('<!-- SIGNUP -->',markup(config))
        if config and config.get('enabled'):
            s=s.replace('</head>','<script type="module" src="signup.js"></script></head>')
            s=s.replace('Subscriptions and sending are inactive. No email address is collected by this preview.','Private signup testing is available below. Public launch and recurring sending remain inactive.')
        p.write_text(s,encoding='utf-8')
