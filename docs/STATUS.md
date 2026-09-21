# Current status

See [PRODUCTION_READINESS.md](PRODUCTION_READINESS.md) for the latest completed work
and remaining gates. The record below describes the first slice only.

# Status — September 21, 2026

## Second slice completed locally

The dashboard now has coordinated region/season selection, an accessible SVG
chart/date inspector/numerical table, open CSV/JSON exports, weekly context,
methods, privacy, and an inactive newsletter section. It displays the frozen
September 21 evidence. Built with Python standard library and browser-native
HTML/CSS/JavaScript; no frontend package or remote font dependencies.

Kit Free is the recommended documented newsletter path under the corrected
privacy rule. See EMAIL_DECISION.md. No account-level validation yet.

Validation: original 10 Python tests pass, 9 JS data/presentation tests pass,
19 browser checks pass. Desktop and mobile screenshots visually reviewed.
Screenshot, report, and portable source/preview are in the task's outputs folder.
Loopback preview: http://127.0.0.1:8765. No production/DNS/schedules/signup/sends.

Next: parameterize accepted daily snapshots with retention/revision/freshness
checks; conduct Kit account-level proof; then prepare hosting/contact/DNS/launch
configuration for approval. Preserve the historical first-slice record below.

## Reviewed twice; implementation begun

The first pass extracted outcomes and fixed constraints. The second checked
dependencies, failure behavior, approval boundaries, and acceptance gaps.
The reference brief is project input adopted by the user's instruction to begin;
it does not authorize purchases, arbitrary messages, DNS changes, or launch.

Confirmed the designated public GitHub repository is empty; cloned that exact
repository without replacing it. No project-specific instructions or existing
source were present. Available Python and Git suffice for the first slice.

Implemented official-data chart/export verification, normalized research CSV/JSON,
and focused tests. Saved real source snapshots. No synthetic production metrics.
The provisional architecture direction is static publication from accepted
snapshots plus hosted scheduled processing; no framework or hosting account has
been committed to before the two feasibility gates are resolved.

## Current gates

- Data: actual exports retrieved and checked against corresponding charts,
  including full historical annual series, reference, units, and calendar dates.
  Geography is identified; coverage/aggregation semantics still need confirmation.
- Email: no verified service meets every constraint yet. Sender excluded;
  Buttondown has a published address conflict; Brevo remains unverified.
- Cost: $0 incurred. Standard-library local work uses existing development access.
  No production $0 operating-cost claim yet: hosting, scheduling, storage, limits,
  and independent missed-run monitoring still need selection and verification.

## Next implementation slice

1. Resolve NRCS coverage/methodology and obtain compatible basin geometry.
2. Build a static statewide + basin dashboard from accepted snapshots with a
   seasonal chart, numerical table, exports, and honest off-season/stale states.
3. Complete the email policy gate before account integration; preserve inactivity
   if incompatible. Continue independent website work.
4. Implement and test snapshot retention, shared edition facts, schedule guards,
   durable delivery state, quotas, and exception alerts.
5. Verify desktop/mobile, keyboard, failure cases, hosted operation, then prepare
   concrete DNS/launch changes for owner approval.

No frontend, production schedule, signup, delivery, DNS, or deployment is complete.
Source changes are local and have not been pushed. See README for reproduction.
