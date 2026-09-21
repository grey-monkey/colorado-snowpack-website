# Bounded email feasibility review — September 21, 2026

> Historical first-slice record. The interpretation below is superseded by the
> user's privacy clarification and [the second-slice review](EMAIL_DECISION.md).
> A provider-supplied compliance address is now acceptable; Grey's personal
> address must remain private. Do not use this old exclusion to reject Buttondown.

**No provider selected or verified end to end. Signup and sending stay inactive.**

| Candidate | Documented free capability | Address constraint / conclusion |
|---|---|---|
| Sender | Not pursued beyond the disqualifying policy | Terms require a valid physical postal address in messages. Excluded under the brief. |
| Buttondown | First 100 active subscribers free; custom sending domain; API available on free plans; registration advertises no card | Published guidance says a physical address is needed and offers a provider address. The brief prohibits any public postal address, so that workaround is not accepted. No documented applicable exemption found. |
| Brevo | Ongoing free plan; 300 sends/day, daily quota does not roll over; branding remains | Public material reviewed did not establish a noncommercial exemption from address requirements. Unverified, not approved. Account/API/footer policy and hard-stop behavior still require proof. |

Sources:
- https://www.sender.net/terms-of-service/
- https://www.buttondown.com/pricing
- https://www.buttondown.com/features/api
- https://marketing.buttondown.email/register
- https://buttondown.com/blog/why-you-need-to-include-a-physical-address-in-your-newsletter
- https://help.brevo.com/hc/en-us/articles/208580669-FAQs-What-are-the-limits-of-the-Free-plan
- https://www.brevo.com/legal/antispampolicy/

Buttondown's address article is old but remains published; it is evidence of a
conflict requiring resolution, not proof that no exception can ever exist.
Brevo's anti-spam page was not extractable in the research browser. Absence of
readable policy is not permission. No support messages have been sent.

The FTC distinguishes message purpose and covers commercial promotion, including
links promoting commercial websites. Keep the site and newsletter informational;
do not treat that alone as blanket legal or contractual clearance.
https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business

## Remaining proof

Need explicit provider-compatible no-public-address operation on the actual free
plan, owner-controlled account approval, approved sender/reply/contact identity,
and a consenting test recipient. Verify signup → confirmation → generated edition
→ test delivery → unsubscribe/suppression → export, plus domain authentication,
tracking settings, footer, plain text, quotas, duplicate prevention, and retries.
No test recipient or credentials have been supplied. DNS and launch approval
remain later steps, after a concrete configuration is ready for review.

Capacity must reserve confirmations/tests and five-edition months. Buttondown's
100-subscriber cap and Brevo's daily send cap are different constraints; neither
establishes automatic safe growth. No paid upgrades, mailbox purchases, borrowed
addresses, or consumer-inbox bulk sending are accepted solutions.

Website/data work can continue. An archive or RSS could be offered separately,
but neither would complete the requested newsletter delivery.
