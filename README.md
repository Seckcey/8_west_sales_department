# 8 West IT Sales Department

The operating system for the 8 West IT sales team, managed in [Paperclip](https://pc.8westit.com).

**Launch status: implementation and internal acceptance are in progress. This repository is not evidence that external outreach is enabled.** See [current status](docs/launch-status.md).

## Team

| Agent | Responsibility |
|---|---|
| [Westy](agents/westy.md) | Sales manager; assigns work, reviews quality, escalates decisions |
| [Scout](agents/scout.md) | Prospect research and source evidence |
| [Quinn](agents/quinn.md) | Qualification and fit scoring |
| [Harper](agents/harper.md) | English and Spanish outreach drafts |
| [Riley](agents/riley.md) | Reply handling, suppression, discovery requests |
| [Morgan](agents/morgan.md) | Solutions, proposals and service handoff |
| [Avery](agents/avery.md) | CRM records, pipeline, reporting and data quality |

Target territories are San Diego, Los Angeles and Baja California, Mexico. Meetings remain requests for owner review; agents do not book calendars. Support offers use discovery followed by a custom quote. The published 8 West IT 365 software subscription prices are **not** prices for managed IT support.

## How to use it

1. Open the **8 West IT Sales** project in Paperclip and give Westy a concrete outcome.
2. Westy routes the work through the specialist team. Review each record's source, fit, next action and owner.
3. Review outreach drafts and meeting requests in the task queue. Mailbox draft creation requires a tested connection.
4. Approve commercial terms for each proposal. A proposal draft is not a signed agreement or a won deal.
5. Read the acceptance record before enabling any scheduled operation or prospect sending.

The initial Claude Code adapter uses the responsible user's existing Claude subscription. Provider limits still apply. No paid API fallback is authorized.

## Contents

- `agents/`: concise versioned role contracts. Paperclip's live managed bundles are maintained separately; deployment is explicit and tracked in the acceptance record.
- `config/department.json`: portable organization, role and capability intent. It is a documented manifest, not an automatic Paperclip importer.
- `docs/`: commercial evidence, operating procedures, integration notes and launch status.
  Start with the [sales playbook](docs/sales-playbook.md).
- `schemas/`: portable prospect contract and validation rules.
- `fixtures/`: fictional test data only, excluded from live reporting and outreach.
- `scripts/` and `tests/`: offline validation for the portable records and launch rules.

## Add another department or model provider

Keep Paperclip as the shared work and approval system. Add a separate project, department manager, instruction bundle and explicit connection grants. Keep the CRM/mailbox as business systems of record; do not move credentials into prompts. Map a new agent to an officially supported adapter and its own authorized funding source. A consumer subscription must not be assumed to include API access. See [architecture](docs/architecture.md).

## Public repository boundary

This repository is public. Commit only reusable instructions, documentation, schemas and synthetic examples. Never commit customer/prospect records, message content, secrets, tokens, OAuth URLs, runtime exports, backups or production `.env` files. Live business data stays in the access-controlled applications.

Run the offline checks with `python -m unittest discover -s tests` and `python scripts/validate_records.py fixtures/prospects.json`.
