# Signup and hosting readiness — progress, September 21, 2026

Status: not yet ready for final public launch approval. The real-recipient lifecycle test passed; remaining technical checks are listed below. Production DNS, public signup and recurring schedules remain unchanged/inactive.

## Implemented and verified

- An email-only inline form uses Kit's native integration with double opt-in. Kit owns subscriber records; the static site receives no private API key and stores no subscriber database. The native form has invisible reCAPTCHA enabled. Default/public preview builds render Opening soon; only the local private rehearsal enables the form.
- Accessible labels, keyboard operation, phone layouts, duplicate-submit protection, slow-response messaging, invalid email and sanitized provider/network errors are implemented. Simulated browser tests exercise these states at 320, 390 and 1440 pixels; these are not substitutes for provider lifecycle verification.
- The owner-approved address was submitted once to the actual Kit form. Kit accepted form membership and the page showed confirmation instructions. A reCAPTCHA connection warning also appeared, so actual abuse-protection behavior still needs resolution. After the owner clicked the confirmation link, Kit independently reported active. No manual reactivation was used.
- The earlier private delivery and unsubscribe proof remains passed, as confirmed by the owner and Kit. Confirmation-editor preview shows Kit's Seattle compliance address. The owner confirmed that the confirmation experience did not show their personal mailing address. The owner reported the generated weekly message and unsubscribe worked. Kit independently confirmed cancelled status and one unsubscribe for the one-recipient broadcast.
- Accepted history now generates concise weekly email HTML/text with source/date, two region summaries, meaningful comparisons and a dashboard link. Private delivery uses exactly one approved active tag member. A durable local SQLite ledger reserves each ISO weekly edition before sending; uncertain attempts and repeat calls are blocked rather than blindly retried. This ledger must be persisted securely before future hosted recurring sending is enabled. No production mailing mode or recurring email job is active.
- Python tests, model tests, dashboard regressions and the new simulated signup-state checks pass. Hosted clean-run tests also passed. Existing stale-data and last-good checks were reused.

## Actual hosting rehearsal

[Temporary HTTPS preview](https://grey-monkey.github.io/colorado-snowpack-website/)

[Successful hosted build](https://github.com/grey-monkey/colorado-snowpack-website/actions/runs/35664249099)

GitHub Pages serves the static site from a public repository. A manual/push-only rehearsal workflow builds on GitHub, refreshes from NRCS and publishes an accepted snapshot. No computer needs to remain on. The preview is publicly reachable and marked noindex; it is not access-controlled. It contains no active signup, custom domain or private configuration. HTTPS, subpath assets, dashboard JSON, supporting pages and full CSV/JSON downloads returned successfully. Hosted active signup is not yet proven; the real vendor submission was from the local test page.

The intended architecture uses GitHub Pages, standard public-repository GitHub Actions, native Kit signup and the existing Kit Free account, with no required paid proxy, database or anti-bot subscription. Kit's account was verified Free with a 10,000-subscriber allowance. Account limits and provider terms still apply; no paid upgrade or new paid service was enabled. The existing domain renewal remains the owner's existing cost.

## Remaining completion gates

1. Passed: owner received and confirmed the double-opt-in email, reported no personal mailing address, and Kit reported active.
2. Generated weekly edition 2026-W39 was sent once through the guarded path. Kit broadcast 26026385 completed with exactly one recipient, public=false, and the private ledger records completion. Passed: owner reported the message and unsubscribe worked; Kit independently confirmed cancelled status and one unsubscribe. Actual returning-subscriber behavior remains to be checked.
3. Resolve the actual CAPTCHA warning and finish hosted signup compatibility/privacy checks without activating public signup.
4. Review the final production activation settings and secure persistence for any future weekly sender; the current sender is deliberately a private proof.

## Domain

Owner confirms ColoradoSnowpack.com is owned and registered at Squarespace Domains. Current authoritative nameservers are Sedo parking. See LAUNCH_DNS.md for exact GitHub Pages records and the Squarespace delegation transition. These instructions have been prepared only; no domain action has been performed.
