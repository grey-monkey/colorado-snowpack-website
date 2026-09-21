# Email decision — revised September 21, 2026

**Recommend Kit Free for the next account-level proof.** A credible $0 path is
documented, including useful initial growth capacity. It is not yet a validated
integration, and subscriptions/sending remain inactive.

The clarified rule protects Grey's personal mailing address from recipients and
the public. Private provider verification and a provider-supplied compliance
address are acceptable. This supersedes the original brief's stricter wording.

## Bounded comparison

| Service | Free scope | Privacy and automation | Decision |
|---|---|---|---|
| Kit Free | Up to 10,000 subscribers; unlimited broadcasts; API access | Offers its compliance address for free; API can create/schedule custom-content broadcasts; export and confirmed opt-in supported | Leading candidate; use our own scheduled generation, not paid visual automation, RSS campaigns, or MCP |
| Buttondown | First 100 active subscribers; API available on free plans | Published guidance offers a provider address; custom domain and export available | Privacy objection is resolved in principle; small cap makes it a fallback for a limited pilot |
| Brevo | 300 sends/day; free branding | Automation capabilities exist, but no provider-address path was established in this review | Lower priority: daily capacity and unresolved public-footer address arrangement |

No account created, no support message sent, and no addresses submitted. Sender's
address requirement remains documented in the historical review, but a private
verification request alone is no longer grounds to exclude any service.

## Why Kit is promising

The current Free-plan article explicitly includes API access and says the Creator
Network can be switched off without changing the free plan. This differs from
legacy Newsletter-plan documentation about a locked recommendation slot. Select
the current Free plan and disable recommendations; verify the actual account.

The broadcast endpoint accepts custom content and a send timestamp; leaving the
timestamp null creates a draft. This supports deterministic recap generation on
our own hosted scheduler without buying Kit automation. Confirm permissions on
the real free account before implementing sending.

Kit's provider address is allowed only for current customers' Kit emails. It is
not an owner postal address, a business location, or a mail-forwarding service.
Do not copy it into the website as Grey's contact information. Confirmation,
broadcast, archive, and account-page settings all need a personal-address audit.

## Capacity and cost guard

At a proposed application cap of 9,500 active subscribers, five weekly editions
would generate 47,500 recipient deliveries, plus confirmations and tests. The
documented unlimited-broadcast allowance is promising, not a claim of unlimited
growth. Plan documentation says exceeding 10,000 requires upgrading to keep
sending. Warn at 9,000 and pause admissions/sending at 9,500 until reviewed.
Implement provider-count reconciliation and a safe gate before exposing forms;
do not assume local counting alone controls hosted-form additions.

Choose the permanent Free plan, not a paid trial. Do not add payment details or
accept an upgrade. Verify the account shows $0 and the boundary behavior before
launch. No billing, quota, or delivery behavior has been exercised on an account.
Hosting/scheduling is outside this provider proof and remains unconfigured.

## Exact next proof

1. Owner creates/approves the Free account and provides verification information
   privately. Record the actual plan and absence of a payment method.
2. Configure accurate approved sender/reply identity and Kit's permitted compliance
   address. Disable the Creator Network and unnecessary tracking where supported;
   document any unavoidable processing in the privacy notice.
3. Use confirmed opt-in forms: confirmation on, auto-confirm off. Do not import or
   directly mark new subscribers confirmed. Keep the form unlisted for testing.
4. Prepare DNS authentication records, preserving existing DNS; obtain authorization
   before changes. Verify SPF, DKIM, DMARC and unsubscribe headers on a real test.
5. Generate one frozen recap, create a private draft via API, inspect footer/plain
   text/HTML, then obtain authorized test delivery to a consenting recipient.
6. Confirm unsubscribe, hard-bounce/complaint suppression, export including relevant
   statuses/consent evidence, and no personal-address leak. Keep durable edition
   state; reconcile uncertain responses instead of blindly duplicating broadcasts.
7. Only after these pass, present the concrete launch configuration for approval.

## Primary sources checked

- [Current Free plan and threshold behavior](https://help.kit.com/en/articles/16627071-the-kit-free-plan)
- [Kit pricing](https://kit.com/pricing)
- [Free provider compliance address and its restrictions](https://help.kit.com/en/articles/2502494-alternatives-for-your-physical-address)
- [Create/schedule a broadcast through API](https://developers.kit.com/api-reference/broadcasts/create-a-broadcast)
- [Double opt-in settings](https://help.kit.com/en/articles/2502655-the-confirmation-email)
- [Suppression and subscriber statuses](https://help.kit.com/en/articles/2502651-the-subscriber-profile-page-and-status)
- [Subscriber CSV export](https://help.kit.com/en/articles/2502489-how-to-export-subscribers-in-kit)
- [Domain authentication](https://help.kit.com/en/articles/2502558-verify-your-domain-to-optimize-your-deliverability)
- [Buttondown free capacity](https://www.buttondown.com/pricing), [API](https://www.buttondown.com/features/api), [provider address](https://buttondown.com/blog/why-you-need-to-include-a-physical-address-in-your-newsletter)
- [Brevo free limits](https://help.brevo.com/hc/en-us/articles/208580669-FAQs-What-are-the-limits-of-the-Free-plan)
