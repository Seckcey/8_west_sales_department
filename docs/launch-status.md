# Launch acceptance

Last updated: 2026-09-25. Setup is in progress; no external prospect outreach is enabled.

| Item | Evidence state |
|---|---|
| Paperclip deployment | Running on Coastline, public authenticated UI |
| Seven-agent roster | Created with role instructions and Claude subscription adapter |
| All specialist workflow tests | In progress; execution and output review still required |
| Department playbooks | Initial documents created; remaining specialist deliverables in progress |
| GitHub repository | Versioned role contracts, playbook, architecture, operations and offline checks prepared for publication |
| HubSpot Free account | Connected through regional MCP endpoint; live get_user_details as Westy succeeded; record writes and dedupe acceptance pending |
| Microsoft 365 account in Zapier | User consent completed |
| Sales mailbox draft tools | Configured with fixed shared mailbox; live call not yet verified |
| Sales inbox reader | Prepared as a fixed GET request; live access not yet verified |
| Zapier-to-Paperclip connection | Approved by owner; token copy from protected browser dialog requires owner paste; no working connection yet |
| Meetings | Owner chose requests only; no calendar writing |
| Support pricing | Custom quote after discovery; no approved standard pricebook |
| Prospect sending | Disabled; no send tools or campaign activated |
| Offline portable-record checks | 10 tests passed; three synthetic regional fixtures validated and excluded from production records |
| Runtime instruction alignment | Live agents have managed instructions; concise repository contracts are not automatically deployed. Westy has received the latest CRM, meeting and pricing corrections |

## Acceptance scenarios

1. Every specialist executes a task using the intended subscription, publishes a result and hands off to the next owner.
2. Three synthetic businesses, one per region, pass through research, qualification, drafting, simulated replies, proposal drafting and CRM export.
3. A duplicate is detected; an unknown price remains unknown; an opt-out cannot advance; a synthetic record cannot be sent or counted in live metrics.
4. CRM read/create/update operates on clearly synthetic records, preserves identifiers and does not create duplicates on a repeated attempt.
5. Sales inbox access is proven on the sales mailbox. Draft creation returns a provider record with `isDraft=true`; no sending occurs.
6. Meeting requests stay in review; no invite is created.
7. Before a prospect campaign, agree the audience, content, sender identity, volume, suppression process and required commercial details. Record actual authorization with the campaign.

Do not substitute a configured setting, an account login or a successful HTTP health response for the relevant acceptance scenario.
