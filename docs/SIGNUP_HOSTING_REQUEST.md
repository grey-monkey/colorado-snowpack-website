# Colorado Snowpack — signup + hosting readiness slice

Continue directly from the completed production-readiness work.

Do not redesign the dashboard, rebuild the data pipeline, or revisit Kit delivery/privacy unless a new issue appears.

Current status:

- dashboard is complete locally
- automated accepted-snapshot pipeline is implemented
- retained history and recovery behavior are implemented and tested
- weekly calculations are implemented
- Kit private API delivery has been tested successfully
- recipient saw Kit’s compliance address rather than Grey’s personal mailing address
- unsubscribe completed successfully
- Kit records the test subscription as cancelled
- public signup remains inactive
- production sending remains inactive
- hosting configuration is prepared but inactive
- nothing has been publicly deployed

The goals of this slice are:

1. Complete the public newsletter signup flow.
2. Verify the subscription lifecycle end to end.
3. Verify the hosting/deployment configuration.
4. Make the project ready for an explicit final launch decision.
5. Do NOT launch publicly without authorization.

---

# 1. Public signup experience

Build and test the actual newsletter signup experience intended for ColoradoSnowpack.com.

The signup should feel like a natural part of the site, not an aggressive marketing funnel.

Keep it simple.

Primary promise:

A concise weekly recap of Colorado snowpack conditions and meaningful changes.

Use your judgment on exact copy and placement.

Prioritize:

- clear value proposition
- minimal fields
- good mobile behavior
- accessibility
- clear success/error states
- no unnecessary profiling questions
- no dark patterns
- no intrusive popups unless there is a compelling UX reason

Email address alone should be sufficient unless Kit genuinely requires something else.

Do not publicly activate the form yet.

---

# 2. Subscription lifecycle

Test the complete lifecycle privately:

visitor enters email
→ signup request succeeds
→ any confirmation/verification step works
→ subscriber becomes active as expected
→ subscriber receives the intended message(s)
→ unsubscribe works
→ subscriber status updates correctly

If double opt-in is used, verify the actual recipient experience.

If single opt-in is used, verify that intentionally and document it.

Do not assume behavior from documentation; test the actual implementation.

---

# 3. Privacy

Preserve the already-validated privacy requirement.

Grey may provide personal account information privately to Kit.

Grey’s personal mailing address must not appear in:

- signup forms
- confirmation pages
- confirmation emails
- newsletter content
- unsubscribe pages
- public archive pages
- website source intended for public exposure
- committed configuration
- logs intended for publication

Verify the complete public-facing subscription path, not just the weekly test email.

Do not commit subscriber addresses or private account information.

---

# 4. Newsletter integration

Connect the signup implementation to the already-tested Kit path in the cleanest practical way.

Do not build a second subscription database unless there is a real need.

Kit should remain the source of truth for subscribers if that is the simplest reliable architecture.

Keep API credentials and secrets outside public source.

The public site must never expose a private API token.

If a backend/proxy is required for secure signup, use the simplest free approach compatible with the planned hosting architecture.

---

# 5. Abuse protection

Add proportionate protection against obvious signup abuse without making signup unpleasant.

The goal is to avoid:

- automated form spam
- accidental repeated submissions
- API misuse
- uncontrolled consumption of free service quotas

Do not introduce paid anti-bot services.

Prefer simple free controls appropriate to the actual risk.

Do not make legitimate users solve an annoying challenge unless necessary.

---

# 6. Signup states

The UI should handle:

- normal successful signup
- already-subscribed email
- invalid email
- temporary network/API failure
- provider failure
- repeated button press
- slow response
- confirmation-required state if applicable

Use clear human language.

Do not expose internal API errors or implementation details to visitors.

---

# 7. Hosting readiness

Verify the prepared free hosting configuration.

The production site should:

- run at $0 in new recurring service cost
- serve the dashboard reliably
- support the automated snapshot architecture
- support any secure signup backend required
- keep secrets private
- support scheduled refreshes later
- handle HTTPS
- work with ColoradoSnowpack.com
- not depend on Grey’s computer remaining online

Do not change production DNS yet.

Do not deploy the real public production site yet unless explicitly authorized.

A temporary/private preview deployment is acceptable only if it does not alter the public domain and does not expose sensitive configuration.

---

# 8. Deployment rehearsal

Perform a deployment rehearsal sufficient to prove that launch should be straightforward.

Verify:

- build succeeds from a clean state
- required environment variables are documented
- secrets are not committed
- production paths resolve correctly
- static assets load correctly
- dashboard data loads correctly
- CSV/JSON downloads work
- signup integration works in the intended hosted architecture
- HTTPS assumptions are correct
- failure behavior remains safe
- scheduled-job configuration is ready but inactive unless testing requires a non-production equivalent

Do not perform unnecessary infrastructure work beyond what is needed to establish launch readiness.

---

# 9. Domain readiness

Prepare the exact DNS/deployment steps that will eventually be needed for ColoradoSnowpack.com.

Do not apply them yet.

At the end of the slice, Grey should be able to approve launch without needing another research phase.

Document only the actual required changes.

Avoid a generic DNS tutorial.

---

# 10. Newsletter presentation

Now that Kit is validated, finish the newsletter-facing design enough for launch readiness.

This includes:

- signup copy
- confirmation messaging
- unsubscribe-compatible footer treatment
- basic weekly email styling
- mobile readability
- source/date clarity
- link back to the dashboard

Do not spend excessive time creating elaborate email graphics.

The newsletter should feel related to the website while remaining robust across email clients.

Keep the actual weekly content concise.

---

# 11. Weekly automation readiness

Connect the already-implemented weekly calculations to the tested Kit delivery path in a non-production/test-safe manner.

Prove that the system can:

accepted history
→ seven-day calculations
→ newsletter content
→ Kit campaign/broadcast payload
→ test delivery

Do not start the real weekly schedule yet.

Prevent duplicate sends.

The eventual weekly automation should have a clear record of whether an edition has already been sent.

---

# 12. Cost check

Reconfirm that the proposed production configuration has:

- $0 new recurring hosting cost
- $0 required newsletter subscription
- $0 required automation service
- no required paid anti-bot product
- no required paid database
- no automatic paid upgrade path

If any free-tier limitation could realistically affect launch or early growth, document it briefly.

Do not optimize for hypothetical massive scale.

---

# 13. Final pre-launch checks

Before calling this slice complete, test the experience on:

- narrow mobile
- typical modern phone width
- desktop
- keyboard navigation
- touch interaction
- signup success
- signup failure
- unsubscribe
- stale dashboard data
- current dashboard data
- CSV download
- JSON download
- newsletter test generation
- newsletter test delivery

Reuse existing tests where possible.

Do not inflate the test count for presentation.

---

# 14. Do not launch yet

This is still a readiness slice.

Do not:

- point ColoradoSnowpack.com to the new hosting
- change production DNS
- activate public signup
- enable production data scheduling
- enable recurring newsletter sending
- announce the site
- send to anyone other than controlled test recipients

Wait for explicit launch authorization.

---

# 15. End-of-slice report

Return a concise report covering:

1. How public signup is implemented.
2. Which opt-in model is being used.
3. Results of the complete subscription lifecycle test.
4. Confirmation that Grey’s personal address remains private throughout the public-facing flow.
5. Hosting platform/configuration selected and why it fits the $0 requirement.
6. Whether signup can run securely on that hosting architecture.
7. Whether weekly generation-to-Kit delivery works end to end.
8. Any realistic free-tier limitations.
9. Exact DNS/deployment actions that would be required at launch.
10. Any genuine blocker remaining.
11. Whether you consider the project technically ready for Grey to authorize public launch.

The desired outcome is:

A fully tested site, signup flow, data pipeline, and newsletter system that is ready to launch with one explicit owner approval — but remains private/inactive until that approval is given.