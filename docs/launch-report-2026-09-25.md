# 8 West IT sales department

> Dated launch handoff from September 25, 2026, retained as historical evidence. This report does not assert current runtime status. Consult [launch acceptance](launch-status.md) and the live task queue for subsequent changes.

Status on September 25, 2026: built and undergoing live acceptance. External prospect sending is not enabled.

## Open the department

- [Paperclip sales build and review queue](https://pc.8westit.com/WES/issues/WES-2)
- [GitHub repository](https://github.com/Seckcey/8_west_sales_department)
- [Sales operating playbook](https://github.com/Seckcey/8_west_sales_department/blob/main/docs/sales-playbook.md)
- [Current acceptance status](https://github.com/Seckcey/8_west_sales_department/blob/main/docs/launch-status.md)

Paperclip runs on Coastline at `/srv/8west/apps/paperclip`, with origin port **3100** and public address **https://pc.8westit.com**.

## Your team

| Agent | Responsibility |
|---|---|
| Westy | Sales manager, priorities and quality review |
| Scout | Sourced prospect research |
| Quinn | Qualification |
| Harper | English and Spanish drafts |
| Riley | Replies, opt-outs and meeting requests |
| Morgan | Discovery scope, proposals and delivery handoff |
| Avery | CRM, deduplication and reporting |

All seven are configured to use the existing Claude subscription. Scheduled heartbeats are off during acceptance; tasks can wake agents on demand. Every specialist still needs a verified end-to-end handoff result before the department is described as operational.

## Accounts and connections

HubSpot, Zapier and Microsoft 365 accounts are already prepared. Do not create duplicate accounts.

**CRM:** HubSpot is connected for Westy and Avery. Avery recorded successful synthetic create/read/update and repeat import with no new duplicates. HubSpot's automatic company creation was then turned off after it generated an extra unmanaged record; a small association check is assigned to Avery. The full role-to-role handoff still needs acceptance.

**Email:** Connected for Westy, Harper and Riley. Westy's fixed lookup of **sales@8westit.com** returned HTTP 200. A Paperclip credential-record defect was repaired without rotating the token or widening access. Harper created one synthetic draft through the approved gateway and Outlook returned `isDraft: true`. Root then verified exactly one matching unsent draft in the shared mailbox's Drafts folder. No send, delete or calendar actions are included. Never paste the protected connection URL in chat or GitHub.

Outlook displays this mailbox's primary address as **sales@8westventures.com** when opened using **sales@8westit.com**. Verify the intended From alias before enabling future sending.

**Meetings:** Requests only, for your review. No automatic bookings or invitations.

## Offers and territories

Target local small businesses in San Diego, Los Angeles and Baja California. There is no industry restriction; employee size is undecided.

Use consultation and a custom quote after discovery. Published IT 365 software subscription rates are not SMB support prices. You approve each quote's scope, price, currency, taxes, hours, response commitments and on-site terms before it reaches a customer.

## What is already verified

- The seven-agent roster, role instructions and subscription configuration exist.
- Every agent has a one-run concurrency setting; scheduled heartbeats are disabled.
- HubSpot authentication and one live agent action passed.
- The Microsoft shared sales inbox read passed as Westy.
- Harper's synthetic draft was created and remains unsent.
- The public repository contains role contracts, a complete concise playbook, architecture, operating procedures and synthetic examples.
- All ten offline record checks passed, including duplicate, suppression, unknown-price and synthetic-exclusion cases. GitHub validation passed.

Offline checks do not prove mailbox access or live CRM writes. The repository contracts are versioned source material; updating GitHub does not automatically replace running Paperclip instruction bundles.

## Remaining acceptance

1. Finish the bounded CRM association check after disabling automatic company creation.
2. Complete each specialist's actual handoff test and review the reconciled live instruction bundles.
3. Before prospect sending, review the concrete campaign, sender alias, suppression process, volume and commercial requirements. No sending capability is currently enabled.

The Zapier connection URL is already saved and the read/draft checks passed. No further paste or token rotation is needed.

The department can keep preparing internal work while these checks finish. Credentials and live prospect records stay in protected applications; the GitHub repository contains only reusable instructions and fictional test data.
