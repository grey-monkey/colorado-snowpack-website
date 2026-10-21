# Weekly scheduling — October 21, 2026

## Finding

`17 15 * * 1` means Monday at 15:17 UTC, year-round. It is 09:17 MDT
in summer and 08:17 MST in winter; it does not mean a fixed Denver wall-clock
time. No timezone conversion or sleep exists in the weekly workflow.

GitHub's run API returned the following values. `created_at` and
`run_started_at` are identical in every case, so these delays occur before
run creation, not during Python generation or newsletter backend processing.

| Run | Intended UTC | Created / run started UTC | Delay |
| --- | --- | --- | --- |
| [36484813408](https://github.com/grey-monkey/colorado-snowpack-website/actions/runs/36484813408) | Sep 28 15:17 | Sep 28 21:14:59 | 5h 57m 59s |
| [37379833927](https://github.com/grey-monkey/colorado-snowpack-website/actions/runs/37379833927) | Oct 5 15:17 | Oct 5 22:02:11 | 6h 45m 11s |
| [38317034633](https://github.com/grey-monkey/colorado-snowpack-website/actions/runs/38317034633) | Oct 12 15:17 | Oct 12 22:30:20 | 7h 13m 20s |
| [39320688399](https://github.com/grey-monkey/colorado-snowpack-website/actions/runs/39320688399) | Oct 19 15:17 | Oct 19 20:36:16 | 5h 19m 16s |

All four used SHA `73614d91860b796ea5ab5d6f2a73a0d60b564396`, event
`schedule`, branch `readiness-preview`, and concluded successfully. For Oct 19,
the job was created at 20:36:17, started at 20:36:20, and completed at 20:36:33.
The job's seconds-long execution cannot explain the preceding five-hour delay.
There are no workflow dependencies or environment approvals in this job.

This identifies GitHub scheduled-event lateness; the API does not expose
GitHub's internal reason for it. Do not claim a particular outage, account
throttle or load incident. GitHub documents that schedule events can be delayed
and even dropped under load. Minute 17 already avoids the top of the hour.
Moving the cron earlier merely guesses at a variable delay.

## Implementation

Use a Cloudflare Cron Trigger in the **existing backend Worker** at the same
UTC time (`17 15 * * MON`) to POST a `workflow_dispatch` to `weekly.yml` on `readiness-preview`.
The existing Python generator, accepted-history checkout, workflow concurrency,
GitHub `WEEKLY_ENABLED` gate, backend `NEWSLETTER_MODE`, authentication and
SQLite-backed `EditionLedger` remain in place. No data/generation port to JS,
new service, new public endpoint, Kit key movement or ledger migration is needed. Cloudflare
uses 1 for Sunday, unlike GitHub; the named weekday `MON` prevents that mismatch.

The scheduler's only new secret is a repository-scoped GitHub dispatch token.
It cannot call Kit or bypass the edition ledger. The handler validates the cron
and scheduled UTC slot, uses a bounded request, rejects redirects, and never
logs credentials or GitHub response bodies. A successful HTTP 200 (or legacy 204) means **dispatch accepted**,
not job success or email delivery. Ambiguous failures are not retried blindly.
The scheduled timestamp is diagnostic only; it never overrides edition identity.

This bypasses the observed late GitHub cron event but still depends on Cloudflare
and GitHub dispatch/runner availability. It is not a real-time delivery guarantee.

## External configuration and cutover

The checked-in Worker mode is `off`; the original GitHub cron stays active
until explicitly switched. Merging alone does not change production scheduling.

1. Merge the change into `readiness-preview`. Create a fine-grained GitHub PAT
   for **only** `grey-monkey/colorado-snowpack-website` with repository
   **Actions: write** (and the mandatory metadata read permission). Give it an
   expiration and track renewal. An independently managed GitHub App installation
   token is an alternative, but requires token refresh outside this small change.
2. Store it in the existing Worker, never a public var or repository file:
   `npx wrangler secret put WEEKLY_DISPATCH_TOKEN --config backend/wrangler.jsonc`.
   Keep existing Kit, automation, hash secrets, provider IDs, asset build and
   Durable Object bindings/migrations exactly as in the current deployment.
   Do not deploy a new Worker name or recreate the ledger.
3. Set `WEEKLY_SCHEDULER_MODE` in the deployment configuration to `dry_run` and
   deploy the existing Worker using its normal complete site/asset build. The
   repository's `backend/wrangler.jsonc` expects `../worker-dist`; this directory
   must contain the normal site build, not an empty placeholder. Review the
   deployment's existing provider ID variables as well: they are not all present
   in the checked-in config and must not be removed by deployment.
4. For a no-broadcast integration check, dispatch `weekly.yml` manually with
   `dry_run=true` on `readiness-preview`. For an actual cron-path check, keep
   Worker mode `dry_run` for Monday Oct 26, 2026, 15:17 UTC. Allow up to 15 minutes
   after deploying for Cron Trigger configuration propagation. Do not use a live
   `wrangler dev --test-scheduled` invocation with production credentials.
5. Verify the new run has event `workflow_dispatch`, `dry_run=true`, the expected
   `scheduled_for`, and `generated_only` in its output. A successful dispatch can
   still yield a skipped job if GitHub `WEEKLY_ENABLED` is not `true`, or fail
   generation if accepted data is stale. Inspect the run, not only the dispatch HTTP status.
   The original GitHub cron continues the normal production send during this
   rehearsal; the Cloudflare dry run submits no edition to the backend.
6. Set Worker `WEEKLY_SCHEDULER_MODE=enabled` and deploy. Confirm GitHub repository
   variable `WEEKLY_ENABLED=true` and backend `NEWSLETTER_MODE=enabled`. Then set
   GitHub repository variable `WEEKLY_SCHEDULER=cloudflare` to skip the original
   GitHub schedule job. Manual dispatch stays available, defaulting to dry-run.
   Enable Cloudflare before disabling the old trigger to avoid a scheduling gap.
   If both fire during cutover, concurrency serializes the jobs and the durable
   edition reservation blocks a second broadcast. A duplicate request may appear
   as a failed workflow because the existing backend returns 409; inspect it.
7. After the next live Monday, compare intended time, Cloudflare dispatch event
   time, Actions `created_at`, job `started_at` and the workflow timing log. The
   next live date depends on when cutover is performed. Confirm the edition's
   backend reservation and Kit broadcast state separately. `sending` is not
   evidence of completed delivery. Observe recipient delivery through Kit's
   reporting; do not create an extra broadcast to test timing.

Use Cloudflare Cron Trigger event history/metrics and GitHub Actions failure
notifications for operational checks. The handler throws sanitized errors for
missing credentials, API rejection or network uncertainty. Existing Worker
observability remains unchanged; use a controlled tail session if detailed
dispatch timestamps are needed. No new alert destination is configured here.

Rollback: unset `WEEKLY_SCHEDULER` (or set it to `github`) in GitHub first, then
set Worker scheduler mode to `off` and redeploy. Preserve all ledger rows,
including uncertain/reserved editions; never clear them to make a retry pass.

## Verification performed and limits

Run locally with no production credentials:

```
node --test tests/weekly-scheduler.test.js tests/hosted-signup.test.js
python -m unittest discover -s tests -p test_send_weekly.py -v
```

Tests mock every outbound dispatch/provider/backend call. They cover UTC slots
on both sides of DST, precise workflow/ref/inputs, dry-run and off modes, backend
mode gating, missing credentials, wrong events, rejected/uncertain dispatch with
no retry, workflow cutover safety, unchanged edition payload/authentication,
and durable no-resend behavior through success, restart and provider timeout.

The static build (`python -m pipeline.build`), all 22 Python tests
(`python -m unittest discover -s tests -v`), all 17 JavaScript tests
(`node --test tests/*.test.js`), and `git diff --check` passed locally.

No production workflow was dispatched or rerun, no backend send was called,
no broadcast was created, and no live Cloudflare deployment or token was
configured during this investigation. Future cron timing and delivery still
require the deployment and observation steps above.

## Primary documentation

- [GitHub schedule limitations](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)
- [Workflow dispatch API and token permissions](https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event)
- [Cloudflare Cron Triggers, UTC and propagation](https://developers.cloudflare.com/workers/configuration/cron-triggers/)
- [Cloudflare scheduled handler](https://developers.cloudflare.com/workers/runtime-apis/handlers/scheduled/)
