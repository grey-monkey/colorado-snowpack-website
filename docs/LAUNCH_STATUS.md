# Colorado Snowpack — public launch

Live URL: https://coloradosnowpack.com/

Status: LIVE. Public signup, twice-daily data retrieval, and Monday newsletter scheduling are enabled. Some browsers may retain the former parking page until their DNS caches expire.

## Production verification

- Final approved layout and latest requested branding are published: the header uses a compact two-line Colorado / Snowpack wordmark with the footer’s bold typeface, tuned spacing and alignment, and no terminal period. The rounded emblem depicts layered snow without a separate underline.
- Apex and www use GitHub Pages’ four IPv4 addresses. All seven email DNS record groups remain present. Nameservers and verified hello forwarding were not changed.
- HTTPS certificate is approved for apex and www; HTTPS enforcement is enabled. Fresh network requests verify HTTP-to-HTTPS and www-to-apex redirects.
- Seventeen live pages/assets/downloads passed HTTPS and protected-value checks. Signup markup points to the encrypted Cloudflare backend. No preview/noindex notices remain on the production pages.
- Public-origin signup reaches Kit. The existing cancelled controlled test subscriber returns the rejoin path and remains suppressed. Invalid requests, the honeypot, unauthorized origins, and protected weekly endpoint checks passed. No new delivery or confirmation claim is made: that full email lifecycle passed during the prior owner-verified proof.
- Production refresh runs succeeded: 35675479628 and 35676039769. The latest accepted NRCS observation is September 21, 2026; repeat retrieval was unchanged. History is retained in the data-state branch.
- Refresh schedule: 06:37 and 18:37 UTC daily. Newsletter schedule: Mondays at 15:17 UTC (9:17 a.m. MDT / 8:17 a.m. MST).
- Hosted newsletter generation verification succeeded: 35675480824, without an extra send. Backend authorization and payload guards are enabled and passed. Durable edition reservations continue to prevent blind duplicate sending.
- 20 Python tests, 12 JavaScript tests, and the 15 responsive/browser checks passed. No redesign or unrelated feature was added during launch; the subsequent explicit logo revision was incorporated.
- Kit API credentials and form identifiers remain encrypted in Cloudflare. The owner separately authorized the automation credential in GitHub Actions’ encrypted secrets. Protected values and known private email addresses were absent from scanned public assets. No personal mailing address was introduced; the prior verified Kit Seattle footer and hello sender configuration remain unchanged.
- New recurring service cost: $0 using the existing free services and public-repository standard runners, within their free-tier limits. Existing domain renewal is separate. No paid plan or overage option was enabled.

## Operation

Repository: https://github.com/grey-monkey/colorado-snowpack-website
Default branch: readiness-preview (name retained; this is now the production source).
Site host: GitHub Pages.
Signup/weekly backend: colorado-snowpack-signup-preview on Cloudflare (existing service name retained to preserve encrypted secrets and durable reservations).

Pause only the affected service: set SNOWPACK_ENABLED=false for retrieval; WEEKLY_ENABLED=false for the newsletter workflow and NEWSLETTER_MODE=off for its backend; SIGNUP_MODE=off for signup. Preserve the weather database and durable edition ledger. Do not change mail DNS when pausing a website service.

The in-app browser still returned a cached parking route during verification, while authoritative DNS, Cloudflare, Google and Quad9 had the production addresses and fresh HTTPS requests served the final build. This is a propagation/cache limitation, not a failed production build.

## Review handoff cleanup

The final approved two-line wordmark uses tighter line spacing and no period. Historic Median appears in the date inspector and numerical table. The mountain caption contains only the title and NPS/D. Turk credit. Production deployment 35676975797 succeeded. Public signup, twice-daily refresh and Monday newsletter switches are enabled; both production workflows are active. The temporary GitHub Pages preview workflow was disabled and moved outside the active workflow directory so it cannot overwrite production. The working tree and source archive are current. DNS cache propagation remains the only temporary visibility caveat.
