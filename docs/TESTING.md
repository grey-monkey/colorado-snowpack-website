# Test evidence — September 21, 2026

Run `python -m pipeline.build`, `python -m unittest discover -s tests -v`, and
`node --test tests/model.test.js`. Result: 10 Python and 9 JavaScript tests pass.
These cover the existing source proof plus missing/zero/near-zero/winter behavior,
frozen and stale data, Denver day boundaries, leap dates, and water-year rollover.

Browser checks in `tests/browser.cjs` use Playwright and installed Chrome. Start
`python preview.py`, set `PLAYWRIGHT_MODULE` to the available Playwright package
if not on the module path, then run `node tests/browser.cjs work/browser`.
Browser testing is a development dependency, not a production service.

19 browser checks passed: real values, bookmarked region changes, year selection,
leap-date inspection, slider keyboard controls, table, skip-link focus, mobile
touch, links/downloads, exported source agreement, and response-failure recovery.
Normal winter, zero, missing, stale, near-zero reference, bad schema, and failed
network cases were simulated with browser request interception. Simulations are
not saved into production snapshots. No browser page errors were observed.

Checked page overflow at 320, 390, 768, and 1440 CSS pixels. Visually inspected
desktop (1440px) and mobile (390px) screenshots. Increased mobile reading text
after review. Chart uses line patterns as well as color, a labeled SVG, keyboard
date inspection, and a full numerical table. Keyboard skip-link focus was fixed.
Touch was emulated in Chromium, not tested on a physical phone. No screen-reader
session, independent accessibility certification, or real email test was performed.

The initial dashboard transfer is about 77 KB uncompressed across HTML, CSS, JS,
and the compact snapshot, plus the small favicon. Full historical CSV/JSON is
loaded only when requested. All runtime fonts/assets are local or system-provided;
the site has no third-party runtime requests, tracking, or package dependencies.

Remaining production tests: automated retrieval/outages/revisions, hosted operation
with workstation offline, scheduling/missed runs, and real signup/authenticated
delivery/suppression/export with the chosen provider. Contact route remains an
owner decision for launch. No production system is claimed complete.
