# Launch acceptance

Last updated: 2026-09-26 UTC. Setup is in progress; no external prospect outreach is enabled.

The [Quinn incident investigation](quinn-runner-incident-2026-09-26.md) traced the failed runs to a Claude authentication category and identified a likely access-token lifetime problem in the installed runtime. Authentication recovery and the sequential specialist handoffs remain pending. Live test starts are also held for Coastline's backup/disk recovery. No runner fix or new provider acceptance is claimed by this documentation update.

| Item | Evidence state |
|---|---|
| Paperclip deployment | Running on Coastline, public authenticated UI |
| Seven-agent roster | Created with role instructions and Claude subscription adapter |
| All specialist workflow tests | Scout's WES-13 is done; Quinn's WES-14 is stalled after three authentication-category failures; WES-15 through WES-18 remain blocked. Resume and output review still required |
| Department playbooks | Initial documents created; remaining specialist deliverables in progress |
| GitHub repository | Published on main; GitHub validation passed at initial commit d082ad0 |
| HubSpot Free account | Connected; Avery's WES-18 evidence reports synthetic create/read/update and repeat import with zero new records. Full role handoff acceptance remains pending |
| HubSpot automatic company creation | Turned off in the account UI after the test exposed an extra unmanaged company; saved confirmation observed. Bounded contact-association follow-up assigned to Avery |
| Microsoft 365 account in Zapier | User consent completed |
| Sales mailbox draft tools | Harper created one synthetic draft through the approved gateway; provider returned isDraft=true. Root verified exactly one matching unsent draft in the shared mailbox's Outlook Drafts folder |
| Sales inbox reader | Fixed GET as Westy returned HTTP 200 from Microsoft with the configured shared-inbox path |
| Zapier-to-Paperclip connection | Connected. Personal credential metadata defect repaired without rotating the token or widening access; see repair record |
| Meetings | Owner chose requests only; no calendar writing |
| Support pricing | Custom quote after discovery; no approved standard pricebook |
| Prospect sending | Disabled; no send tools or campaign activated |
| Outgoing sender alias | Future acceptance needed: the requested sales@8westit.com mailbox opens with primary address sales@8westventures.com in Outlook. Do not infer the final From identity from successful draft creation |
| Offline portable-record checks | 10 tests passed; three synthetic regional fixtures validated and excluded from production records |
| Runtime instruction alignment | Westy reports consolidating all seven managed instruction files and reconciling the repository process reference. Repository edits still do not automatically deploy to runtime |

## Acceptance scenarios

1. Every specialist executes a task using the intended subscription, publishes a result and hands off to the next owner.
2. Three synthetic businesses, one per region, pass through research, qualification, drafting, simulated replies, proposal drafting and CRM export.
3. A duplicate is detected; an unknown price remains unknown; an opt-out cannot advance; a synthetic record cannot be sent or counted in live metrics.
4. CRM read/create/update operates on clearly synthetic records, preserves identifiers and does not create duplicates on a repeated attempt.
5. Sales inbox access is proven on the sales mailbox. Draft creation returns a provider record with `isDraft=true`; no sending occurs.
6. Meeting requests stay in review; no invite is created.
7. Before a prospect campaign, agree the audience, content, sender identity, volume, suppression process and required commercial details. Record actual authorization with the campaign.

Do not substitute a configured setting, an account login or a successful HTTP health response for the relevant acceptance scenario.

Mail setup evidence and maintenance limits: [connector repair record](connector-repair-2026-09-25.md).
