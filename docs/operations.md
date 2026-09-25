# Operations

## Deployment

- Host: `coastline`
- App directory: `/srv/8west/apps/paperclip`
- Compose definition: `/srv/8west/apps/paperclip/compose.yaml`
- Local origin: `http://127.0.0.1:3100`
- Public UI: `https://pc.8westit.com`
- App container: `eightwest-paperclip`
- Database container: `eightwest-paperclip-db`

The runtime and database are separate persistent services. Read the host's private `OPERATIONS.md` before maintenance. Do not copy `.env`, database storage, instruction runtime exports or backups into this public repository. Windows Docker Desktop is not part of this deployment.

## Normal review

Review tasks requiring owner decisions; overdue next actions; records missing sources; duplicates; replies and opt-outs; proposal gaps; failed runs; subscription/tool usage; and the current connector grants. Report real prospects separately from synthetic tests. Zero activity is a valid result, not a reason to fabricate progress.

## Pause or incident

1. Stop the affected Paperclip run and disable its routine or connection. Preserve the task, error category and timestamp.
2. If a message send result is uncertain, inspect the provider's sent state before retrying. Never resend merely because the response was lost.
3. An opt-out immediately stops all outreach to that address. Preserve the minimum suppression evidence; do not treat a reopened deal as renewed permission.
4. If credentials may be exposed, revoke/rotate them in the provider and update the protected connection. Never paste credentials into an incident task.
5. Resume after the specific failing acceptance test passes. Record the evidence and owner decision.

## Backup and recovery

Paperclip's configured database backup runs hourly with seven-day retention on the same host. This is not an off-host disaster-recovery copy. Verify backup timestamps and a separate restoration test before treating recovery as proven. Do not stop or restore the live database as a test; use an isolated Coastline project and a separate database.

## Repository versus runtime

Versioned instructions are concise role contracts. Updating a Markdown file in GitHub does not change a running agent. Deploy managed instruction bundles through Paperclip, verify each role's effective settings, and update the acceptance record. Preserve prior instruction versions for rollback. Do not edit the application database to change agent state.
