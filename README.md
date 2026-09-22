# ColoradoSnowpack.com

Colorado's snowpack, made clear.

The dashboard supports validated live retrieval, accepted history and last-good
publication. A temporary GitHub Pages rehearsal is available with signup disabled;
production DNS and recurring schedules remain inactive. Signup lifecycle verification
is still in progress. See [current readiness](docs/FINAL_HOSTED_STATUS.md) and
[prepared Squarespace DNS instructions](docs/LAUNCH_DNS.md).

For accepted data (Python 3.11+):

```sh
python -m pip install -r requirements.txt
python -m pipeline.run
python preview.py
```

`tzdata` supplies the Denver time zone on Windows. Production uses a hosted
runner later; the prepared workflow is inactive. The frozen research build below
remains available for reproducibility and the original browser regression tests.

## Open the local dashboard

```sh
python -m pipeline.build
python preview.py
```

Open http://127.0.0.1:8765. The server binds only to loopback and serves `dist/`.
Stop it with Ctrl+C. The portable bundle includes a prebuilt `dist/`; only the
second command is needed to preview that build. Do not open index.html directly
as a file: browsers block its module/data requests. Build files can later be
hosted statically; a temporary hosting rehearsal has now passed.

The browser consumes `data/snapshot.json` schema 1.0.0; automated accepted
snapshots can use the same interface without redesign. The current build input
is deliberately pinned to frozen, hash-checked evidence. Read
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
