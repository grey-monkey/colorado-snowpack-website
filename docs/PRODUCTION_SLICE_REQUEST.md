# Colorado Snowpack — production-readiness slice

Continue directly from the completed dashboard slice.

Do not redesign or rewrite the working dashboard unless this slice exposes a real problem. Preserve the verified UI, tests, data verifier, documentation, and accepted decisions.

The goals of this slice are:

1. Replace the frozen research-only flow with a safe automated accepted-snapshot pipeline.
2. Prove outage/staleness/recovery behavior.
3. Privately validate Kit Free as the newsletter delivery path.
4. Leave the project ready for a later production deployment decision.

Do NOT deploy the public site, modify DNS, start scheduled production jobs, or activate public newsletter signup/sending without explicit authorization.

---

# 1. Automated accepted snapshots

Build the production-oriented data path that can retrieve the same official NRCS products already validated and turn them into accepted dated snapshots for the dashboard.

The principle should remain:

official NRCS source
→ retrieval
→ validation
→ accepted snapshot
→ dashboard / exports / weekly calculations

Do not let newly downloaded data replace the last accepted snapshot merely because retrieval succeeded.

A snapshot should only become public/current after passing the important validation rules already established.

Reuse the existing verifier and tests wherever practical rather than creating a parallel validation system.

---

# 2. Safe failure behavior

The website must fail conservatively.

If fresh data cannot be retrieved or validated:

- retain the last accepted valid snapshot
- clearly indicate that the data is stale
- preserve the observation date
- do not replace missing/error values with zero
- do not publish malformed or partially trusted data
- do not make the site unusable simply because the newest refresh failed

Prove recovery as well:

failure
→ last good snapshot remains available
→ later valid retrieval succeeds
→ new snapshot becomes accepted normally

Avoid complicated infrastructure if simple reliable behavior accomplishes this.

---

# 3. Data status and provenance

Make sure the system can distinguish important states such as:

- current accepted data
- stale accepted data
- failed retrieval
- failed validation
- missing source data
- frozen/test data

The public interface does not need to expose developer jargon.

It should simply communicate what a normal visitor needs to know.

Keep enough internal metadata for debugging and reproducibility.

---

# 4. Historical storage

Retain accepted dated observations in a clean form suitable for:

- dashboard history
- seasonal charts
- weekly recap calculations
- CSV / JSON exports
- future research use

Do not design a large database system unless the actual workload requires one.

Choose the simplest durable approach that fits the existing project and free-operation constraint.

Avoid unnecessary duplication of large source artifacts.

---

# 5. Automation design

Prepare the refresh process so it can later run unattended on free hosted infrastructure.

Do not require Grey’s personal computer to remain on for normal production operation.

The production target remains:

- $0 new recurring service cost
- reliable scheduled refreshes
- understandable failure handling
- easy owner recovery
- no surprise paid upgrades

You may choose the implementation and hosting mechanism.

Do not activate production scheduling yet.

If a free-tier limit or operational constraint matters, document it briefly.

---

# 6. Kit Free — private validation

Kit Free is currently the leading newsletter candidate.

Do not treat documentation alone as sufficient.

Perform the smallest practical private end-to-end validation needed to establish whether Kit actually satisfies this project.

Grey is willing to:

- create the account
- provide a real mailing address privately to Kit
- verify identity or email ownership
- authenticate a sending domain if needed
- provide DNS changes when specifically requested
- receive test emails
- install free tools/plugins if useful

The key privacy requirement remains:

GREY’S PERSONAL MAILING ADDRESS MUST NOT BE VISIBLE TO NEWSLETTER RECIPIENTS OR THE PUBLIC.

Kit may privately store or verify the address.

What must be tested is what recipients actually see.

---

# 7. Kit proof

Validate, as practical on the free plan:

- account creation
- signup/subscriber capability
- API access needed for the intended workflow
- ability to create/send a test broadcast automatically or through an appropriate free integration
- unsubscribe behavior
- subscriber exportability
- provider compliance-address behavior
- recipient-visible footer/content
- whether Grey’s personal address appears anywhere in an actual received message
- any required Kit branding
- current free-plan limits that materially affect this project
- whether the core weekly automation can remain $0

Use a private test recipient.

Do not activate a public signup form yet.

Do not send anything to real subscribers.

If Kit requires Grey to perform an interactive login, verification, DNS action, or other owner-only step, stop only at that specific step and ask for it clearly.

Do not restart broad newsletter-provider research unless Kit fails an actual requirement.

If Kit does fail, document exactly why before evaluating the next-best candidate.

---

# 8. Weekly recap foundation

You may prepare the internal weekly-calculation layer using accepted snapshots.

Do not spend significant effort polishing newsletter prose yet.

The important part is proving that the system can reliably calculate a clearly defined seven-day recap from accepted data.

The future newsletter should derive its facts from those calculations rather than asking an AI model to infer changes from charts.

Keep deterministic calculations separate from optional future writing/presentation logic.

Do not activate automated weekly sending yet.

---

# 9. Off-season behavior

Preserve the dashboard’s current correct handling of zero historical medians and shoulder-season conditions.

The automated pipeline must not reintroduce misleading percent-of-median values.

Test at least:

- zero same-date median
- normal nonzero winter median
- missing observation
- measured zero
- stale data
- failed retrieval
- invalid incoming value
- successful recovery after failure

Do not add unnecessary seasonal complexity beyond what is needed for correct behavior.

---

# 10. Testing

Extend the existing tests only where this new functionality creates meaningful risk.

Important things to prove:

- valid retrieval can become an accepted snapshot
- invalid retrieval cannot replace the last accepted snapshot
- stale-data status behaves correctly
- recovery works
- repeated execution does not corrupt history
- dates and water-year transitions remain correct
- missing and zero remain distinct
- dashboard continues working from accepted snapshots
- exports remain internally consistent
- weekly calculations use the intended reporting interval
- private Kit test behavior matches the privacy requirement

Do not inflate the test count simply for appearance.

---

# 11. Security and privacy

Do not commit:

- passwords
- API tokens
- private mailing addresses
- subscriber email addresses
- private account details

Use appropriate local/environment secret handling.

The repository should remain safe to publish from a secrets/privacy standpoint.

Do not place Grey’s personal mailing address in source code, fixtures, screenshots intended for public use, logs committed to Git, or documentation.

---

# 12. Efficiency

Work forward from the existing implementation.

Do not:

- redesign settled UI
- repeatedly research settled data questions
- rebuild the verifier
- create speculative infrastructure
- optimize for huge scale
- write excessive process documentation

Do:

- reuse what works
- validate the actual risky parts
- make decisions and proceed
- keep architecture proportionate
- preserve quality
- leave the project understandable for future work

Efficiency means avoiding redundant work, not lowering the standard.

---

# 13. End-of-slice report

When complete, return a concise report covering:

1. How automated retrieval and accepted snapshots now work.
2. How failed/stale updates are handled.
3. How recovery was tested.
4. Where accepted history is stored and why.
5. Whether the system is ready for unattended free hosting.
6. Kit Free validation results.
7. Exactly what a test recipient sees regarding address/footer/privacy.
8. Whether Kit appears viable for the real weekly newsletter at $0.
9. Whether weekly calculations are ready.
10. Any genuine blocker requiring Grey’s action.
11. Your recommended next slice.

Include useful evidence or screenshots where they clarify a result, but do not create a large report for its own sake.

The desired outcome is:

A dashboard whose data pipeline can safely operate unattended, plus a proven private newsletter-delivery path, ready for a later decision to deploy publicly.