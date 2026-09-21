# Production-readiness status — September 21, 2026

## Data path

`python -m pipeline.run` retrieves both official JSON products and their matching
charts with bounded time/size/retries. It reuses the existing verifier for every
annual/reference value. Units, calendar validity, nonnegative finite numbers,
current water year, chart/JSON agreement, matching product dates and source age
must pass before a transaction can accept a release. Future values, lost history,
date regression and excessive newly missing history are rejected.

Accepted records are stored in `state/snowpack.sqlite`: one initial observation
set, changed rows thereafter, release metadata/source hashes, and each refresh
attempt. Historical releases can be reconstructed exactly with `read_release`.
This uses Python's built-in SQLite; no hosted database subscription. The first
real release contains 29,567 dated observations and occupies about 11.8 MB.
Future-date null placeholders are excluded; missing historical values remain null.
A second real retrieval returned unchanged, with zero duplicated observations.

Publication builds complete release-specific files before atomically switching
the dashboard entry. Dashboard, CSV/JSON and weekly facts share the same release.
Failure retains the last accepted data and observation date. A separate health
file explains an unsuccessful update; an unavailable health file never hides
readings. The browser independently marks observations older than two Denver
calendar days as overdue, including when a refresh job never runs. Frozen builds
remain explicitly frozen. No accepted release means an existing site stays intact.

Weekly facts compare the accepted end date with exactly seven calendar days
before it. Missing endpoints withhold the comparison/delivery eligibility; zeros
remain measurements. Percent-of-median changes are percentage points and omitted
when either reference is below 0.1 inch. Net SWE change is not snowfall. Facts and
presentation are separate. No production sending is implemented or enabled.

## Validation

17 Python tests, 9 JavaScript model tests, the existing 19 browser checks and a
new accepted-release browser check pass. Covered: real accepted inputs, repeated
runs, outage, bad values, stale/missing source, zero vs missing, winter reference,
leap day/year boundary calculations, exact weekly interval, immutable earlier
release, matching exports, retained UI, health-file outage and successful recovery.
Synthetic changes exist only inside tests, never in the public or accepted store.
Actual live retrieval and repeat execution also passed on September 21.

## Hosted operation — prepared, not deployed

Target: a public GitHub repository, standard Ubuntu Actions runner, and GitHub
Pages for the informational static site. `ops/refresh-workflow.yml.disabled` is
inert: outside the workflow directory, disabled extension, no schedule. It needs
an initialized `data-state` branch with the accepted SQLite database, Pages setup,
and an explicit `SNOWPACK_ENABLED=true` repository variable before activation.
The job serializes execution, persists history before deploying, publishes last
good data after rejected updates, and ends failed to expose the problem. It stops
at 40 MB database / 50 MB site sizes instead of adding paid infrastructure. Only
current public release files are built on each clean hosted runner; full accepted
history stays in the data-state branch. The state branch contains public weather
data only, never subscriber data or credentials. Back it up before maintenance.

For a later approved launch: pin action revisions, initialize state, enable Pages,
review permissions/budgets and execute one manual hosted acceptance run. Then add
twice-daily off-the-hour scheduling and verify GitHub failure notifications plus
an independent missed-run check. Neither hosted execution nor missed-run alerts
has been proven yet. It requires no owner PC once hosted, but is not launch-ready
until those checks are complete. Disable the workflow or set SNOWPACK_ENABLED to
false to pause. Re-run manually after an upstream outage; do not edit observations
to force acceptance. Inspect safe attempt reasons and upstream products. Restore
an earlier database from the state branch only after investigating corruption.

[GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
says public-repository standard runners are free. The template refuses private
repositories. [Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)
include a 1 GB site and 100 GB/month soft bandwidth limit. The prepared build is
far smaller. Keep the artifact for one day; do not enable paid overages or larger
runners. Review storage use and Git history growth before launch and periodically.
[Scheduled events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)
can be delayed/dropped and public-repository schedules can stop after 60 days of
inactivity. Freshness must never depend only on a successful job status.

## Kit private proof

Owner-created account visibly shows **Free, 10,000 subscribers, $0/month**.
Owner approved the named V4 API key and use of the verified account email.
Credentials, recipient and API responses are in ignored `private/`, not public
builds or deliverables. Kit API successfully authenticated and retrieved account,
forms, templates and subscribers. Only the consenting owner was added as a test
subscriber, tagged separately; this is not proof of public double opt-in signup.
The private API draft succeeded. Before sending, the tag filter was checked to
contain exactly the authorized address. Kit's eventually consistent tag listing
initially lagged, so the send guard stopped until membership was visible.

Kit's provider address was saved through email settings. The actual draft preview
shows `600 1st Ave, Ste 330 PMB 92768, Seattle, WA 98104-2246`, Unsubscribe,
Update your profile and Built with Kit. One broadcast was created/sent through
V4 with `public=false`; API later reported completed, 1 recipient, 100% progress.
No public post, public signup or production schedule was enabled. A CSV export
of the private test subscriber succeeded and is kept only in `private/`.
A local send-attempt ledger prevents blind duplicate sends after uncertain results.

**Private delivery/privacy/unsubscribe proof passed.** On September 21, 2026,
the owner reported inspecting the actual received message: it showed Kit's Seattle
address and no personal mailing address. The owner clicked its unsubscribe link
and saw successful unsubscribe. A subsequent authenticated API check independently
returned subscriber state `cancelled`; broadcast statistics reported one recipient,
one opened email and one unsubscribe (100%). Recipient-visible address evidence
is the owner's direct report, not an independent inspection of the raw message.
The subscriber remains cancelled; no further test message was sent.

Kit is viable for the tested $0 API delivery path, including provider-address
privacy, recipient unsubscribe and private subscriber export. Public confirmed
opt-in, consent records, bounce/complaint suppression, sending-domain authentication,
tracking/recommendations policy, quota boundary behavior and durable weekly-send
reconciliation remain prelaunch checks. No DNS changes were made. Recommend
completing those launch checks and reviewing a concrete hosted deployment next;
public deployment, signup and production sending still require authorization.

[Kit address policy](https://help.kit.com/en/articles/2502494-alternatives-for-your-physical-address)
permits the provider address for current users' Kit email marketing only; it does
not forward mail or packages. [Broadcast API](https://developers.kit.com/api-reference/broadcasts/create-a-broadcast)
supports private broadcasts with tag targeting. See `EMAIL_DECISION.md` for prior
research; this file supersedes its statements that no account/API proof exists.
