# Sales operating playbook

This is the concise process reference. Paperclip stores task execution and approvals; HubSpot stores accepted CRM records; Microsoft 365 stores actual mailbox drafts.

## 1. Research — Scout

Start with a small, named batch and territory. Use the business's own website and other permitted public professional sources. Capture the page, observation date and the specific fact supported. Never fabricate an email from a naming pattern or buy a list without authorization.

Check normalized email and company domain against existing records and the suppression register. Unknown contact information stays empty. Hand the sourced record to Quinn.

## 2. Qualification — Quinn

Use the [customer profile](ideal-customer-profile-v0-1.md). Distinguish evidence, assumptions and unanswered questions. Explain the fit in two or three sentences and name the best next action. An opt-out stops the record regardless of fit. Hand suitable records to Harper; return specific evidence gaps to Scout.

## 3. Outreach drafting — Harper

Write for one business and one relevant topic. Use verified facts and avoid implying an existing relationship. Show draft language, recipient source, subject, body and the reason for the contact. Do not promise pricing, availability, compliance or service levels.

English starter, for internal customization:

> Subject: IT support for [business]  
> Hello [name], I'm reaching out from 8 West IT. We help small businesses with everyday IT support, Microsoft 365 and network needs. [One accurate, sourced reason this may be relevant.] Would you be open to discussing your current setup? We can prepare a custom quote after understanding the scope. If you prefer no further contact, please let us know.

Spanish starter, for internal customization:

> Asunto: Soporte de TI para [empresa]  
> Hola [nombre]: Le escribo de 8 West IT. Ayudamos a pequeñas empresas con soporte de TI, Microsoft 365 y redes. [Un motivo relevante y verificado.] ¿Le interesaría conversar sobre sus necesidades? Podemos preparar una cotización después de definir el alcance. Si prefiere no recibir más mensajes, indíquenoslo.

These are unfinished drafts. Before sending, add the verified sender identity and required business/address/disclosure details, remove placeholders, confirm the applicable outreach requirements and record campaign approval. The Spanish wording does not promise Spanish-language service delivery.

Suggested cadence for owner review: an initial message, one useful follow-up after five business days, and a final close-out after another seven. No cadence is scheduled now. Any reply, opt-out, bounce or unresolved delivery result stops the pending sequence.

## 4. Replies and meetings — Riley

| Reply | Action |
|---|---|
| Interested | Draft acknowledgment and collect discovery needs |
| Requests pricing | Explain that scope is needed for a custom quote; route to Morgan |
| Requests a meeting | Record preferred times, time zone and participants for owner review |
| Opt-out or negative contact instruction | Suppress immediately; cancel pending follow-ups; notify Avery |
| Wrong person | Update contact evidence; do not assume a referral permits sending |
| Bounce | Hold the address and investigate; do not guess alternatives |
| Legal complaint, security issue or sensitive attachment | Stop the sequence and escalate privately |
| Ambiguous | Hold for review; do not treat silence or ambiguity as consent |

Read only the sales mailbox through the approved connection. Initial lookup returns message previews, not full bodies or attachments; request owner review where the preview is insufficient. Create replies only after verifying the message and mailbox. Draft creation is not sending.

Meeting packet: business/contact, requested times and time zone, topic, participants, current systems, urgency, questions and owner decision. No calendar invitation.

## 5. Discovery and proposals — Morgan

Ask about staff and sites, current provider, Microsoft 365 use, devices, network issues, onboarding/offboarding, backups, security needs, business hours, desired outcomes and decision process. Do not collect passwords or unnecessary sensitive data.

Proposal structure:

1. Business needs and supporting discovery notes.
2. Proposed work, deliverables and exclusions.
3. Dependencies and customer responsibilities.
4. Open questions.
5. Owner-approved price, currency, taxes, terms and service commitments.
6. Proposed start and acceptance process.

Keep section 5 explicitly unapproved until Frankie resolves it. Price objections prompt scope clarification; they do not authorize discounts. Incumbent-provider objections prompt questions about unmet needs; never disparage a competitor or invent comparisons.

A won deal requires recorded customer acceptance of approved terms and delivery-owner acceptance. Create a handoff containing scope, agreement reference, contacts, assets in scope, dates, dependencies and open risks. Never put credentials in it. Lost reasons: no fit, no timing, no budget confirmed, selected another provider, no response after authorized sequence, or other with evidence. Suppression remains separate from a lost reason.

## 6. CRM and reporting — Avery

Use stable internal IDs alongside HubSpot IDs. Search before creating. Repeat an import as an update to the same record, not a new record. Preserve the most restrictive suppression state during any merge; unresolved identity conflicts go to review.

Pipeline mapping:

| Stage | Entry / exit requirement | Owner |
|---|---|---|
| Researched | Dated source and territory; exit after fit review | Scout |
| Qualified | Fit rationale and questions; exit with draft brief | Quinn |
| Pending confirmation | Missing owner decision; exit when recorded | Westy |
| Approved for outreach | Exact campaign and content approval; actual sends still require an available authorized tool | Westy |
| Contacted | Provider evidence of a real send; never use a draft as proof | Riley |
| Replied | Verified reply; exit with next action | Riley |
| Discovery scheduled | Owner confirmed a real meeting; requests stay pending | Riley |
| Scoping | Discovery evidence and open requirements | Morgan |
| Proposal drafted / approved | Separate draft from owner-approved terms | Morgan / Frankie |
| Won / lost | Documented outcome and reason; won requires delivery handoff | Avery |
| Suppressed | Stop instruction; cannot exit through ordinary stage changes | Riley / Avery |

HubSpot's free default deal pipeline may combine early prospect stages. Keep detailed prospect state on contact/company properties or a structured note when a property is unavailable. Do not buy another pipeline or change unrelated data to force the mapping.

The repository's small JSON contract is an offline exchange/preflight format, not a complete HubSpot model or automatic importer. Map to the live CRM deliberately, validate first and keep business data out of this public repository.

## 7. Review and limits — Westy

During rollout: scheduled heartbeats off, one specialist at a time, one concurrent run per agent, bounded tasks, no paid API fallback. Prefer completing a useful small result over expanding documentation.

Daily on an authorized run: review new replies/opt-outs, overdue actions, missing evidence, duplicates, proposals awaiting decisions and failures. Weekly on an authorized run: summarize qualified prospects, discovery requests, approved proposals, wins/losses, backlog age, subscription limits and tool usage. A draft is not a sent email; an API acceptance is not inbox delivery.

Exclude all synthetic records from production counts. Avoid mailbox polling: Zapier MCP calls consume tasks, and the current free allowance is small. Recheck the actual account allowance before scheduling.

## 8. Acceptance and pause

Each specialist must execute and publish a result. Use three clearly synthetic records with reserved example addresses. Exercise duplicate detection, missing pricing, opt-out stop, meeting requests and won-deal handoff. Test CRM create/read/update without duplicates, and prove a mailbox draft has isDraft=true. Record failures honestly.

For any wrong recipient/mailbox, permission failure, exposed secret, unexpected charge or uncertain send: stop the affected action, preserve minimal evidence and notify Westy. Do not retry uncertain sends. Follow [operations](operations.md).
