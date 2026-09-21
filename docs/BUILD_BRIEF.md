# ColoradoSnowpack.com — Astra Build Brief

**Final consolidated handoff · September 21, 2026 · Supersedes all earlier briefs.**

## 1. The assignment

Build a small, beautiful, dependable Colorado snowpack resource: a daily dashboard, an automatically produced and delivered weekly newsletter, and openly accessible data. Make it understandable to an interested Coloradan and useful to a researcher without forcing either into the other's interface.

**Working promise: Colorado's snowpack, made clear.**

A visitor should quickly understand the statewide picture, explore a basin, and see how the season compares. A subscriber should learn what changed without needing to visit the site. Grey should not need to write reports, copy data, or press Send every week.

You own the design and engineering decisions. This brief fixes the outcomes and constraints, not the palette, framework, component tree, or exact layout. Deliver a polished, working product—not a disposable prototype. Achieve efficiency by avoiding unnecessary work, not by skipping quality.

## 2. Fixed owner requirements

**Repository and domain.** Use `https://github.com/grey-monkey/colorado-snowpack-website` for `ColoradoSnowpack.com`. Inspect existing work and project instructions first; preserve them. Do not create a replacement repository. Keep source, pipeline, templates, tests, and deployment documentation here. The repository does not dictate the hosting provider.

**No new recurring service costs.** Hosting, scheduling, storage, newsletter delivery, and required operating tools must fit ongoing free plans—not trials, temporary credits, or paid add-ons. No paid newsletter subscription, automatic upgrades, metered overages, or routine paid model calls. Prefer no-card plans with enforceable limits; warnings alone do not prevent charges. Existing domain renewal, computer/internet, and already-held development access are outside this incremental budget. No purchases or additional credits are authorized.

**Informational and noncommercial.** Remove the earlier monetization plan completely. No sponsorship slots, advertising, affiliate offers, paid products, commercial lead generation, or subscriber-list sales. This is an independent information project, not a claimed government service, registered nonprofit, or Colorado office. Any later commercial direction requires Grey's new approval and a fresh compliance review.

**No public postal address.** Do not add a postal address to the website or newsletter templates, and never expose Grey's address in archives, source, or logs. Do not invent an address or location. Private provider verification is separate: explain any requirement and let Grey supply or approve real information privately. Do not buy a mailbox or accept a public-address requirement on Grey's behalf.

**Available resources.** Grey authorizes project work using the computer on which Astra is installed and its available programs/plugins, and is willing to download useful free tools. Inspect actual capabilities, reuse suitable tools, and check licenses. Protect unrelated files and accounts; do not expose the home computer, weaken security, or bypass permissions. Production should run while the workstation is off, without an open Astra session.

## 3. Resolve two dependencies before investing heavily

**Data proof.** Validate one statewide series and one basin series against the corresponding official NRCS product, including current values, reference baseline, historical comparison, units, dates, and aggregation/geography. NRCS offers machine-readable access and basin products; that does not establish that the complete intended integration already works. [3][4]

**Email proof.** Find a genuinely free, policy-compatible delivery service and prove the required path: signup → confirmation → programmatically produced edition → authorized test delivery → unsubscribe/suppression → export. Verify API or equivalent supported automation access, custom content, domain authentication, quotas, required footer/branding, address rules, and account approval on the actual free plan.

The FTC's commercial-email rules depend on message purpose; a genuinely noncommercial newsletter is different from commercial promotion. Removing ads is not blanket clearance under every law or provider contract. Review the actual content, linked site, and required footer. **Sender is not an accepted default: its published terms require a valid physical postal address in messages.** Do not circumvent that requirement. [1][2]

Make a bounded comparison, then choose one suitable service. If no verified option meets both the free-operation and address constraints, report the exact conflict early. Continue independent website work, but keep email signup/sending inactive until resolved. An archive or RSS feed may be proposed as an interim option, not silently substituted for the requested newsletter or presented as complete delivery.

## 4. The website experience

**Immediate understanding.** Show the latest statewide snowpack comparison—normally percent of the same-date median where meaningful—with a plain-language explanation, observation date, and useful recent change. Make the reference period and underlying SWE easy to find where supported. Say “latest available,” not “live.” Put useful information ahead of decoration.

**Regional relevance.** Provide an intuitive basin view, preferably a lightweight map with an equivalent selectable list. Basin selection should coordinate with the summary and chart and have a bookmarkable URL. Use authentic boundaries matching the data; no location permission or visitor account is needed.

**Seasonal context.** Create one excellent seasonal chart comparing the current season, previous season, and historical reference. Clearly label units, periods, and missing data. Provide an accessible table or equivalent numerical view. Add a few meaningful computed weekly takeaways rather than a wall of metrics.

**A reason to subscribe.** Explain the weekly email's benefit, show a real recent edition when available, and offer a straightforward signup. Before a real edition exists, label any demonstration honestly. No popups, invented audience counts, or email gates around public measurements.

**Design freedom, real quality.** Aim for an original, calm, credible, mountain-informed publication. Choose the visual identity and layout. Give typography, hierarchy, charts, spacing, interaction feedback, and desktop composition the same care as mobile. Support touch, keyboard, screen readers, sufficient contrast, and non-color status cues. Handle loading, empty, error, stale, and off-season states as finished parts of the design. No decorative feature should impair speed or comprehension.

Keep navigation small. Include weekly archives, data/methods, privacy, and a working owner-approved contact route. Add the ordinary finishing details: crawlable pages, meaningful titles, canonical URLs, sitemap, favicon, and sharing previews. Avoid manufactured daily articles and near-duplicate location pages.

## 5. The weekly newsletter

**Promise: The week's Colorado snowpack changes, explained in about a minute.**

Start with one statewide edition: a clear takeaway, compact regional comparison, a useful visual when appropriate, and a few meaningful changes. Include the reporting interval, source attribution, and a link to explore further. The email itself should deliver value. Roughly 250–350 words is a starting point, not a quota.

Prefer Monday morning in `America/Denver`, with the exact timing based on source availability. Define the seven-day comparison precisely and handle daylight saving without changing source observation dates. Preserve weekly delivery during low-snow months with an honest, shorter off-season edition rather than fabricated excitement.

Write from verified calculations using polished templates. Do not generate seven daily AI articles and summarize them. Avoid unsupported causes, forecasts, superlatives, or claims about skiing, avalanche safety, runoff, or water supply. Snow-water loss during melt season is not automatically a deterioration in conditions.

Render email and public archive from the same frozen edition facts. Support readable email with images disabled and a plain-text alternative. Never expose subscriber-specific links or unsubscribe tokens in the public archive.

## 6. Data accuracy and open access

Use official NRCS products as the starting point, with provenance and methods accessible from the site. Colorado's official FAQ documents historical/API access and basin geometry; use compatible products rather than mixing similarly named regions. [3][4]

Prefer published aggregates. Any reconstruction must follow a documented method and be checked against the matching official output. Never invent a statewide result by averaging basin percentages, silently change station populations between comparisons, or describe a station-based index as a measurement of every unit of water across Colorado.

Explain snow water equivalent as water contained in snow, not snow depth. State the actual reference statistic and period; do not interchange mean, median, or percent of seasonal peak. Separate SWE change from percentage-point change: 80% to 90% is 10 percentage points, not evidence of 10% more stored water. Net SWE change is not fresh snowfall.

Keep missing values distinct from zero. Define sensible treatment of zero/near-zero reference values, partial coverage, stale readings, and revisions. Align seasonal comparisons consistently, including rollover and leap dates. Distinguish observation dates from retrieval timestamps. Synthetic data belongs only in clearly marked tests/demos, never the production status.

Provide no-login CSV and JSON for the same statewide/basin series used on the site. Simple downloadable files are sufficient. Include stable identifiers, units, dates, baseline, source attribution, actual historical coverage, quality flags, and a versioned schema/method. Add a small loading example and verified reuse guidance. Preserve published edition snapshots and label corrections to historical series. Link deeper station-level research to upstream tools rather than building a second research platform.

## 7. One small, dependable operating system

`Official data → validation → stored snapshots → dashboard + exports + weekly edition → delivery service`

Choose the simplest maintainable architecture meeting the requirements. A static-first site with scheduled processing and modest persistent storage is a reasonable starting point, not a prescribed stack. Use supported integrations, cache shared data, and avoid making each visitor query the upstream service. Use the workstation for heavy initial preparation when useful.

Daily jobs retrieve, validate, and publish accepted data. Weekly jobs calculate the agreed interval and send the validated edition once. Keep durable edition/send state; reconcile uncertain provider responses before retries. Delays and retries must not produce duplicate campaigns or silently omit recipients.

Retain the last valid data during outages, visibly flag staleness, and delay/suppress a materially unreliable email rather than guess. Include bounded retries, a pause switch, private diagnostics, and exception-only owner alerts. Detect missed runs with a check that does not depend solely on the job it watches. Ordinary publication must not require manual approval after launch.

Document real free capacity, including five-edition months, confirmations, tests, storage, execution, and sending limits. Warn before limits and stop safely before any billable action. Do not evade quotas with extra accounts or substitute personal-inbox bulk sending/home mail servers. Keep the public site useful when email is paused. Make export, recovery, and replacement of the delivery service straightforward without speculative multi-provider engineering.

## 8. Subscriber trust and operational security

Collect only the email and consent information needed at launch. Require confirmed opt-in, explain frequency/use, provide easy unsubscribe, and honor bounce/complaint suppression. Do not add profiling, advertising trackers, or unnecessary preference surveys. Explain actual data processing in the privacy notice; protect subscriber records separately from public snowpack data.

Use accurate sender identity, a working reply/contact route, authenticated domain sending, and appropriate unsubscribe mechanisms. Verify SPF, DKIM, DMARC and delivery behavior against current provider/recipient requirements. [5]

Keep credentials server-side and outside source control, public builds, and logs. Protect signup and sending endpoints against abuse. Retain only necessary consent/suppression records. Use owner-controlled accounts and secret stores. Obtain needed login, installation, DNS, and launch approvals; preserve existing DNS/email configuration and unrelated work. Test delivery only to consenting recipients before activating public subscriptions and scheduled sends.

## 9. Work efficiently without lowering the standard

Resolve feasibility, select one coherent direction, and build a working end-to-end slice before expanding it. Research current constraints and unfamiliar integration details—not every possible framework. Reuse reliable components where they fit; invest custom effort in the experience and data presentation.

Keep a short decision/status record so sessions resume without rediscovery. Make focused changes, use targeted tests, and reserve an explicit visual/UX refinement pass. Avoid repeated whole-project rewrites, redundant agent reviews, elaborate project-management machinery, and verbose progress narration. Do not revisit sound decisions without new evidence.

Ask Grey only for consequential decisions, credentials/permissions, or genuine blockers. Make ordinary reversible choices yourself. Cut extra features before cutting data verification, accessibility, mobile refinement, or end-to-end testing. No visitor accounts, chatbot, custom forecasting, full CMS, station-level GIS, bespoke mail server, or personalization platform at launch.

## 10. Acceptance and handoff

**Prove correctness and operation.** Check production numbers against source products and all outputs against shared snapshots. Exercise winter, melt season, off-season, missing/zero/stale data, revisions, time boundaries, quotas, scheduler failure, retries, duplicate-send prevention, and unsubscribe suppression. Verify hosted operation with the workstation offline. Distinguish actual tests from simulations and untested assumptions.

**Prove the experience.** Inspect rendered mobile and desktop screens, not only code. Test touch/keyboard use, readable charts, empty/error states, downloads, signup, confirmation, email rendering, and unsubscribe end to end. Confirm no fabricated metrics, public postal address, leaked credentials/subscriber data, broken primary controls, or accidental paid dependency.

**Deliver ownership.** Provide working source/deployment configuration, a short setup and pause/recover/export guide, dated service limits/terms, an explicit $0 incremental operating-cost account, and concise test evidence. Clearly separate completed work, live integrations, and owner-blocked steps. A deployed frontend alone is not the finished system. Do not claim a guarantee of unlimited free growth or zero maintenance.

**Success: clear enough to understand quickly, credible enough to cite, beautiful enough to bookmark, useful enough to keep receiving—and manageable without becoming another weekly job for Grey.**

## Official reference starting points

Consult these only where needed; recheck applicable terms at implementation. No vendor is mandated.

[1] FTC, CAN-SPAM compliance guide (commercial purpose and address requirements): `https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business`

[2] Sender, Terms of Service, General Rules (message postal-address requirement; checked September 21, 2026): `https://www.sender.net/terms-of-service/`

[3] USDA NRCS, Snow and Water Products Guide (REST access, basin products, compatibility caution): `https://www.nrcs.usda.gov/programs-initiatives/sswsf-snow-survey-and-water-supply-forecasting-program/snow-and-water-products`

[4] Colorado Snow Survey FAQ (historical data, APIs, basin definitions/geometry, data issues): `https://www.wcc.nrcs.usda.gov/ftpref/support/states/CO/products/faq/`

[5] Google, Email sender guidelines (authentication, subscription and unsubscribe practices): `https://support.google.com/a/answer/81126?hl=en`
