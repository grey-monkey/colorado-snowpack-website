# ColoradoSnowpack.com

Colorado's snowpack, made clear.

The dashboard supports validated live retrieval, accepted history and last-good
publication at [ColoradoSnowpack.com](https://coloradosnowpack.com/).
The [public launch record](docs/LAUNCH_STATUS.md) documents production DNS,
GitHub Pages hosting and public signup through the Cloudflare backend.
`readiness-preview` is the default branch and production source despite its name.

## Operational status — October 28, 2026

- **Data refresh and publication:** GitHub scheduling is active. The
  [refresh workflow](.github/workflows/refresh.yml) is configured for 06:37 and
  18:37 UTC daily. The [October 28 scheduled run](https://github.com/grey-monkey/colorado-snowpack-website/actions/runs/40696691205)
  succeeded, including validation, accepted-history persistence and GitHub Pages
  deployment. Accepted history is retained on `data-state`.
- **Weekly newsletter:** The [October 26 run](https://github.com/grey-monkey/colorado-snowpack-website/actions/runs/40396323304)
  executed successfully with event `schedule`. It started at 20:30:55 UTC,
  5h 13m 55s after the configured Monday 15:17 UTC slot. This verifies GitHub
  scheduled execution, not completed email delivery; backend edition state and
  Kit delivery reporting require separate verification.
- **Cloudflare scheduling:** The October 21 implementation is present, but
  production activation remains unverified. The checked-in
  [Worker configuration](backend/wrangler.jsonc) sets `WEEKLY_SCHEDULER_MODE=off`;
  it does not establish the deployed setting. The
  [weekly workflow](.github/workflows/weekly.yml) retains GitHub cron, gated by
  `WEEKLY_ENABLED=true` and skipped for scheduled events when
  `WEEKLY_SCHEDULER=cloudflare`. See the [cutover instructions](docs/WEEKLY_SCHEDULING.md)
  for external configuration and verification.
- **Signup readiness:** The [September 21 hosted readiness report](docs/FINAL_HOSTED_STATUS.md)
  records a passed controlled signup, confirmation, test delivery and unsubscribe
  lifecycle. The launch record documents subsequent public signup checks.
  These are historical verification results, not a new lifecycle or delivery test.

The readiness report and [September 21 DNS instructions](docs/LAUNCH_DNS.md)
preserve pre-launch findings and plans; their inactive-service statements are
not current operational status. Consult the launch record for the documented
production setup.

For accepted data (Python 3.11+):

```sh
python -m pip install -r requirements.txt
python -m pipeline.run
python preview.py
```

`tzdata` supplies the Denver time zone on Windows. The active refresh workflow
runs on a GitHub-hosted runner. The frozen research build below remains available
for reproducibility and the original browser regression tests.

## Open the local dashboard

```sh
python -m pipeline.build
python preview.py
```

Open http://127.0.0.1:8765. The server binds only to loopback and serves `dist/`.
Stop it with Ctrl+C. The portable bundle includes a prebuilt `dist/`; only the
second command is needed to preview that build. Do not open index.html directly
as a file: browsers block its module/data requests. Production static files are
published to GitHub Pages by the refresh workflow.

The browser consumes `data/snapshot.json` schema 1.0.0. The local
`pipeline.build` research build is deliberately pinned to frozen, hash-checked
evidence; the production `pipeline.run` flow uses validated retrieval and accepted
history. Read
[email decision](docs/EMAIL_DECISION.md) and [test evidence](docs/TESTING.md).

## Run the data proof

Python 3.11+; install requirements.txt for the accepted-flow time zone tests.

```sh
python -m unittest discover -s tests -v
python -m pipeline.proof --input evidence/2026-09-21 --output work/proof
```

The proof compares all historical annual and 1991â€“2020 median values in two
official NRCS JSON exports with their matching daily chart traces. It then emits
JSON/CSV observations and a provenance report with source URLs and SHA-256 hashes.
No source observations are reconstructed from basin percentages.

Read [the status and decisions](docs/STATUS.md), [data method](docs/DATA_METHOD.md),
and [email feasibility findings](docs/EMAIL_FEASIBILITY.md) before continuing.
The supplied owner brief is preserved in `docs/BUILD_BRIEF.md`.

This checkout belongs to https://github.com/grey-monkey/colorado-snowpack-website.
The repository was empty when inspected on September 21, 2026.

## Weekly newsletter scheduling

See [weekly scheduling](docs/WEEKLY_SCHEDULING.md) for the delayed-run
investigation, Cloudflare dispatch setup, no-broadcast rehearsal and rollback.
