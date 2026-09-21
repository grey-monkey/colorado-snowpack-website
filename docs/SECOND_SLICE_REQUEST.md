# Colorado Snowpack — next implementation slice

Continue from the completed first implementation slice. Do not restart or redo work that is already verified unless new evidence shows that something is actually wrong.

The first slice established a good data-validation foundation. Preserve the existing verifier, frozen evidence, normalized exports, tests, documentation, and decision history.

The priorities now are:

1. Build the first polished dashboard experience from the accepted data.
2. Resolve enough of the NRCS aggregation/coverage semantics to label the public data correctly.
3. Re-open the newsletter-provider investigation using the clarified privacy requirement below.
4. Keep everything aligned with the existing project brief, $0 recurring-cost goal, and designated GitHub repository.

Repository:
https://github.com/grey-monkey/colorado-snowpack-website

Source changes may remain local until deployment is specifically authorized.

---

# 1. Dashboard

Proceed with the first polished, mobile-first ColoradoSnowpack.com dashboard.

The site should feel like a finished public information product rather than a developer dashboard or raw data viewer.

The primary user question is:

“How is Colorado’s snowpack doing?”

The answer should be immediately understandable, with supporting detail available without clutter.

Use the project brief as the authority for product goals, but exercise your own judgment on:

- visual identity
- typography
- colors
- layout
- chart style
- responsive behavior
- framework
- component architecture
- implementation details

Do not treat previous layout suggestions as rigid wireframes.

Aim for something attractive, trustworthy, restrained, fast, and useful enough that a Coloradan would genuinely bookmark it.

Prioritize:

- excellent phone experience
- clean desktop scaling
- fast load
- clear information hierarchy
- accessible charts and controls
- understandable language
- high visual polish
- minimal unnecessary interface complexity

Avoid generic weather-site clutter, needless widgets, excessive decoration, and features that do not improve the core experience.

---

# 2. Current-data behavior

The September 21 research snapshot established:

- statewide SWE: 0.0443478261 inches
- Colorado Headwaters SWE: 0.0516129032 inches
- the same-date historical median for both is zero

Therefore a percent-of-median comparison is not meaningful for those observations.

The public interface must handle this correctly.

Do NOT display:

- misleading percentages
- infinity
- divide-by-zero artifacts
- a fabricated “0% of median”
- comparisons that imply more than the source data supports

Create a thoughtful off-season / shoulder-season state.

When percent-of-median is not meaningful, the interface should communicate that naturally. Raw SWE may still be shown when useful, while the comparison can be presented as unavailable or not meaningful for that date.

Use judgment on the exact language and presentation.

Missing values must remain distinct from measured zero.

Clearly show:

- observation date
- units
- source
- whether data is current, stale, frozen, or otherwise limited

Do not present the current frozen research snapshot as a live production feed.

---

# 3. NRCS semantics / correctness gate

The remaining station-coverage and aggregation questions matter because the public dashboard must accurately describe what its statewide and basin values represent.

Investigate these questions enough to confidently label the public product.

Do not turn this into an open-ended research project.

The goal is not to independently validate every sensor or reconstruct NRCS methodology from first principles. The goal is to avoid making claims that the official products do not support.

If a specific interpretation remains uncertain:

- use narrower wording
- document the limitation
- avoid the unsupported claim
- continue building everything else that is not blocked

Do not let one unresolved wording issue unnecessarily halt the rest of the dashboard.

If basin data can be represented confidently, expand beyond Colorado Headwaters.

If not, it is acceptable for the first polished build to use a smaller verified scope rather than display a complete-looking map with questionable semantics.

Correctness is more important than apparent completeness.

---

# 4. Architecture

Build the interface so it can later consume accepted automated snapshots without needing a redesign.

Keep the architecture simple.

The intended production model remains approximately:

official data
→ validation
→ accepted dated snapshot
→ dashboard/public exports
→ weekly recap generation

Do not introduce infrastructure merely because it might become useful later.

The public data requirement remains important:

- CSV
- JSON
- understandable metadata
- source attribution
- units
- dates
- quality/status information where appropriate

But do not build an elaborate developer portal in this slice.

A data scientist should eventually be able to get the underlying published series without scraping charts or providing an email address.

---

# 5. Newsletter — clarified address/privacy requirement

The weekly newsletter remains part of the product.

The previous interpretation of the mailing-address requirement was too strict.

Grey IS willing to provide a valid real mailing address privately to an email-service provider for:

- account creation
- verification
- compliance
- account administration
- sending authorization

That is acceptable.

The privacy requirement is:

GREY’S PERSONAL MAILING ADDRESS MUST NOT BE VISIBLE TO NEWSLETTER RECIPIENTS OR THE PUBLIC.

Do not expose Grey’s personal mailing address in:

- newsletter footers
- newsletter body content
- public newsletter archives
- ColoradoSnowpack.com
- public metadata
- public account pages

A provider may know or store the address privately.

The problem is recipient-visible/public disclosure, not private provider verification.

Therefore, re-evaluate newsletter options using the correct criteria.

Do not reject a provider simply because it asks Grey for an address privately.

Reject or avoid a provider if using it would require Grey’s personal address to appear to subscribers or publicly.

A provider-supplied compliance address or another solution that keeps Grey’s personal address private is acceptable if it meets the rest of the project requirements.

---

# 6. Newsletter-provider requirements

Find the best practical $0 option that supports the intended workflow.

Important requirements:

- $0 recurring subscription cost
- no temporary trial disguised as a free solution
- supports a growing real mailing list at useful scale
- signup / opt-in workflow
- unsubscribe handling
- reasonable deliverability
- API, automation, SMTP, or another reliable way to send the weekly recap automatically
- Grey’s personal mailing address is not visible to recipients
- exportability of subscriber data
- no forced paid automation tier for the core weekly workflow, unless the same workflow can be implemented ourselves at $0
- no unexpected automatic upgrade or charge

Provider branding on a free plan is acceptable if it is reasonably unobtrusive.

Grey is willing to:

- create accounts
- verify identity
- provide an address privately
- configure DNS when needed
- install free tools
- install free plugins
- let you use the development computer and available installed software for the project

Do not incur a charge or subscribe to a paid service without explicit authorization.

If no newsletter provider clearly satisfies the requirements yet, document the best candidates and the exact blocker rather than repeatedly researching the same options.

Do not let the newsletter-provider question block dashboard development.

---

# 7. Newsletter product

The intended newsletter is still:

Colorado Snowpack Weekly

Its purpose is to summarize the week’s verified snowpack changes automatically and make the underlying dashboard more useful.

The newsletter should eventually be:

- concise
- factual
- easy to scan
- genuinely informative
- useful even without clicking through
- based on the same accepted data used by the website
- generated automatically
- sent automatically

A reasonable target remains roughly a one-minute read.

Do not generate unsupported weather predictions, ski-condition claims, water-supply guarantees, or sensational interpretations from snowpack measurements alone.

Prefer verified computed facts.

AI may eventually improve wording, but routine operation should not require expensive model usage if deterministic calculations and templates can accomplish the task well.

Do not activate public signup or sending until the provider/privacy path is actually validated.

You may design the website so the newsletter naturally fits into the experience.

---

# 8. Commercial content

For now, ColoradoSnowpack.com and the newsletter should remain informational and noncommercial.

Do not build:

- ads
- sponsorship placements
- affiliate links
- paid memberships
- paid reports
- ecommerce
- commercial email promotions
- subscriber monetization infrastructure

We can revisit monetization later if desired.

Do not spend implementation time preparing for hypothetical commercial features.

The current goal is to build a useful audience by making an excellent resource.

---

# 9. Cost constraint

The project should operate with $0 in new recurring service costs.

This does not mean sacrificing quality.

It means choosing architecture intelligently.

Avoid:

- paid newsletter subscriptions
- unnecessary SaaS
- paid automation tools when a free implementation is practical
- required ongoing paid AI generation
- automatic paid upgrades
- infrastructure that exists only because it is convenient rather than necessary

Existing domain ownership, the development computer, existing internet access, existing development access, and already-available tools are outside this new-service-cost requirement.

If a free-tier limit could become relevant, document it clearly.

Do not spend time optimizing for hypothetical huge scale before the site has an audience.

---

# 10. Efficiency

Do excellent work efficiently.

Efficiency does NOT mean:

- rushing
- skipping testing
- producing a visually mediocre product
- ignoring accessibility
- avoiding necessary research
- stopping at the first technically functional version

Efficiency DOES mean:

- reuse the verified first-slice work
- avoid repeatedly rereading or researching settled questions
- avoid rewriting working systems for stylistic reasons
- avoid speculative architecture
- avoid unnecessary dependencies
- make decisions and move forward
- investigate blockers only to the depth needed to resolve them
- keep documentation concise and useful
- test the important things rather than generating excessive process artifacts

Use your judgment.

You are not expected to follow previous design suggestions mechanically. Improve on them where you see a better solution.

---

# 11. Testing expectations

Before calling this slice complete, verify the dashboard behaves correctly across realistic conditions, including:

- current September / near-zero SWE
- historical median equal to zero
- measured zero
- missing observation
- stale snapshot
- normal winter values
- leap dates where applicable
- water-year transitions
- narrow mobile screens
- typical desktop screens
- touch interaction
- keyboard accessibility where relevant
- chart readability
- loading/error states

Preserve and extend the existing automated tests where they add meaningful protection.

Do not create tests purely to inflate test count.

---

# 12. Deployment

Do not deploy production, modify DNS, activate scheduled production jobs, expose signup publicly, or begin sending newsletters unless explicitly authorized.

Local previews and local testing are encouraged.

Keep the project organized so deployment can later be straightforward.

---

# 13. End-of-slice report

When this slice is complete, return a concise implementation report covering:

1. What was built.
2. What the dashboard now looks and feels like.
3. What data is displayed and exactly how it is labeled.
4. How the zero-median/off-season condition is handled.
5. What was confirmed about statewide/basin aggregation semantics.
6. What newsletter solutions were evaluated under the corrected address/privacy requirement.
7. Whether a viable $0 newsletter path has been identified.
8. Mobile/desktop/accessibility testing performed.
9. Any genuine unresolved correctness or deployment issues.
10. Your recommended next implementation slice.

Include a usable local preview and/or screenshots if available.

Do not produce a giant report for its own sake. Give enough evidence to understand the work and make the next decision.

The goal of this slice is a high-quality dashboard foundation and a clear newsletter path — not maximum feature count.