# Quinn runner incident and handoff recovery

Status: diagnosis complete; authentication recovery and live handoff acceptance pending. Read-only observations on September 26, 2026 UTC cover Quinn's September 25 failures. No runtime setting, credential, task status, provider record or sending permission was changed by this investigation.

## Finding

Quinn's `acpx_turn_failed` error is a Claude authentication failure category. In the message `ACP agent reported a terminal access failure`, **terminal means the turn ended**, not access to a shell or terminal. Changing filesystem permissions or replacing the terminal tool is not a supported remedy for this evidence.

The installed `claude-agent-acp` 0.73.0 maps `auth_required` to the typed AIR failure category `access`, with a `login` recovery action. Its provider-error mapping sends `authentication_failed` and `oauth_org_not_allowed` to that category. Paperclip's ACPX patch then replaces the structured failure with the generic message above; its execution adapter records `acpx_turn_failed`.

An expired copied access token is the leading explanation, **not a confirmed provider rejection reason**. The connection was saved at 10:41:26 UTC, and the first failed turn ended at 18:41:47 UTC, approximately eight hours later. The installed Claude local-login importer returns only `claudeAiOauth.accessToken`. The runtime injects that value through `CLAUDE_CODE_OAUTH_TOKEN`; Anthropic is excluded from the credential-file refresh/writeback path. The isolated sign-in directory is removed after connection creation, and the saved credential remains at version 1.

The retained run logs do not distinguish expiry, revocation, or an organization-access rejection. Raw provider tracing was not enabled for these runs, and their temporary provider transcript directories no longer exist. Do not report a specific HTTP status, expiry timestamp, quota exhaustion, or provider outage without new evidence.

## Evidence

Verified deployment: Coastline, `/srv/8west/apps/paperclip`, app image `ghcr.io/paperclipai/paperclip@sha256:a02ac35ac41df911af477422ea0e781cf41d2b2c600c66f0a5ac9d8c63f52c2c`. The app and database were running without an OOM flag; origin health returned HTTP 200. These checks do not prove subscription authentication.

| Quinn run | UTC start and finish, September 25 | Observed outcome |
| --- | --- | --- |
| `7d17c882-f1a6-499f-8843-cdd0b0b790e2` | 18:23:37–18:41:47 | Multiple successful terminal operations, followed by typed access failure |
| `a5a7507b-4379-4668-b2e9-b215276d057c` | 18:42:47–18:42:52 | Fresh session ended with the same failure |
| `0ae91c58-4534-433d-8f15-56751f39bc3d` | 18:43:47–18:43:52 | Fresh session reported zero token usage, then the same failure |

The saved account, **My Claude subscription**, was active and enabled, with health marked `ok` but no recorded health-check timestamp. Treat this as saved configuration, not current provider acceptance. All seven sales roles use the responsible user's Anthropic subscription; the shared account may therefore affect other roles too. That impact has not been tested by starting them.

Installed-code evidence, inspected without editing the container:

- `packages/adapters/claude-local/node_modules/@agentclientprotocol/claude-agent-acp/dist/session-failure-extension.js`: `AIR_FAILURE_POLICY` and `providerFailureCategory`.
- `patches/acpx@0.13.1.patch` and `patches/acpx@0.12.0.patch`: `typedTerminalSessionFailureCategory` and the generic thrown error.
- `packages/adapter-utils/src/acpx-engine/execute.ts`: terminal settlement and `acpx_turn_failed` recording.
- `server/dist/services/local-ai-credentials.js`, `server/dist/services/ai-connection-runtime.js`, and `server/src/services/local-ai-login.ts`: token import, runtime binding and login-home cleanup. The corresponding source and deployed JavaScript paths were cross-checked for the relevant behavior.

These files belong to the deployed upstream application. The public `Seckcey/paperclip` repository currently contains operations documentation; it is not the application source or a deployment mechanism. This report does not contain an upstream fix.

## Preserve before recovery

WES-14 remains `in_progress`, despite no queued or running agent at inspection. Existing issue documents must not be replaced by a fresh generic dry run:

| Document key | Revision at inspection | Updated UTC, September 25 |
| --- | --- | --- |
| `continuation-summary` | 5 | 18:43:52 |
| `dryrun-qualification` | 2 | 17:58:20 |
| `rubric-v220-body` | 1 | 18:37:19 |
| `rubric-v220-ruling` | 1 | 18:21:40 |

The failed run performed further preparation after some of these publications. Reconcile the current documents, continuation summary and any surviving prepared work before publishing. A prepared rubric body is not evidence that the authoritative rubric was updated. Preserve document revisions and require a fresh read before each write.

## Supported recovery and its limits

1. Obtain a refreshed host-capacity and recovery-baseline window from the backup/host owner. Coastline initially reached 95% used with about 25 GiB available. After the protected sync finished and its cleanup ran around 02:35 UTC, a fresh check showed 86% used and 63 GiB available. The urgent capacity hold was lifted, but this sync's Paperclip pack failed. The coordinator reviewed the isolated restore below and released the existing-account reconnect step. A live Quinn run still requires verified authentication and current sequencing. Do not touch backup staging, restart services or repair/retry the separate backup job as part of runner recovery.
2. After the shared-operation hold permits authentication recovery, sign in to Paperclip as the owner of **My Claude subscription**. Open **Apps**, select that existing connection and use **Reconnect** in its AI account controls. Keep the existing subscription method, personal owner, connection target, agent grants and default selection. Do not revoke the identity, create a duplicate connection or select a paid API fallback.
3. The local-environment flow creates an isolated sign-in attempt and displays its exact `CLAUDE_CONFIG_DIR` / `claude auth login` command. Run that generated command as the application user in the existing Paperclip environment on Coastline. It must run in the same filesystem context as Paperclip, not on the Windows desktop. Complete the provider's normal browser sign-in/MFA when requested. Never paste tokens, authorization codes or login URLs into GitHub or routine task comments.
4. Return to the connection flow, allow its verification to become ready, then choose **Connect**. The installed check calls Anthropic's usage endpoint before saving. Verify that the original connection/grant and intended scope are preserved. A successful reconnect proves only credential acceptance at that time; it does not pass Quinn or the handoffs.
5. Resume exactly one bounded, fresh Quinn run against WES-14, with an idempotency key and no scheduled heartbeat. Preserve the current subscription/provider, no-send restrictions and existing documents. Stop after one authentication failure rather than blindly retrying. If needed, collect a bounded protected provider trace, retaining only sanitized failure category/status in this repository.

The reconnect path is verified from `ManagedAiConnectionDetails.tsx`, `AiConnectionAccountControls.tsx`, `AiConnectionCredentialStep.tsx`, `useLocalAiLogin.ts`, and the installed local-login routes/services. It has **not been executed or accepted in this investigation**. Opening the reconnect flow itself creates a login attempt; it is not a read-only status check.

A fresh local sign-in may restore a limited work window, but it still imports only the access token in this installed version. It does not repair refresh persistence or prove durable unattended operation. A permanent upstream credential-lifecycle repair or a different officially supported subscription sign-in method needs separate source review, isolated validation and an authorized release. Never copy another application's credentials or silently change the funding source.

### Recovery baseline and stop conditions

The app-managed hourly backup `paperclip-20260926-021611.sql.gz` is 7,981,449 bytes. Its gzip integrity check passed. The decompressed stream identifies the Paperclip JavaScript backup format, was created at 02:16:11.722 UTC, contains 211 table definitions and 10,261 inserts, and ends with `COMMIT` and the expected statement delimiter. This matches the installed `packages/db/src/backup-lib.ts` writer. The original protected instance master-key file exists; its contents were not read or exported.

An isolated PostgreSQL 17 restore was then executed from 02:39:06 to 02:39:12 UTC with `psql -X -q -v ON_ERROR_STOP=1`; it exited 0. It recovered 211 tables (210 public plus one migration table), 7 agents, 39 issues, 94 documents, 256 document revisions, 8 connection grants, 14 secrets and 110 heartbeat runs. Those counts matched the live read-only comparison. All four WES-14 document revision numbers and content hashes matched. The restored secret-version count was 128 versus 132 live, so this is not a claim that every row matches the current database; the selected Claude credential remained version 1 in both.

The restore used task-owned Compose project `quinnrestore01a0db84`, a dedicated volume, no network or published ports, no application, and a 512 MiB / 0.5 CPU cap. After verifying the ownership labels, its container and volume were stopped, removed and confirmed absent. The original backup, key and production database were untouched. Production app/database remained running without OOM; disk remained 86% / 63 GiB and available RAM was approximately 3.9 GiB.

This proves the SQL backup can be restored into a separate database and preserves the inspected sales state. It does **not** prove application boot, credential decryption, full filesystem restoration or an off-host recovery. The failed shared backup pack remains a separate gap. No real provider call or agent run was made by the restore test.

Reconnection updates the existing encrypted credential version, connection health metadata and scoped login-attempt state. It must preserve the connection, grant, agent grants and default identity, and does not require rewriting business documents. Inspect those identities before and after. A failed reconnect must not trigger deletion/recreation of the connection or a whole-database rollback. Stop and preserve the error without exposing credentials. Do not restore a known-invalid old credential merely to make metadata look unchanged.

After successful authentication, the first Quinn run is one bounded fresh attempt on WES-14. Stop on authentication failure, changed permissions/provider, unexpected external action, or an unresolved handoff dependency. Keep document revisions for targeted recovery. Do not automatically advance Harper until Quinn's actual publication and handoff have been reviewed.

## Sequential handoff acceptance

Use one specialist at a time. Before each step, check current task dependencies, active runs and the previous deliverable. Stop on a concrete unmet dependency. Completing a dry-run gate test does not grant external sending authority.

| Step | Required artifact and reviewed evidence |
| --- | --- |
| Quinn, WES-14 | `dryrun-qualification`: per-dimension evidence/UNKNOWN, confidence, duplicate collision and surviving ID, preserved history, pending-confirmation route, disqualification rationale and reconciled rubric version; explicit handoff to Harper |
| Harper, WES-15 | `dryrun-outreach`: English and Spanish synthetic drafts, follow-up hard stop, missing-token fallback, claim ledger and unresolved commercial placeholders; every draft marked not sent; handoff to Riley |
| Riley, WES-16 | `dryrun-replies`: labelled simulated reply cases, opt-out suppression surviving re-import, pricing/bounce/hostile routing, named approver, meeting request only and no invitation; handoff to Morgan |
| Morgan, WES-17 | `dryrun-proposal`: discovery evidence, unknown commercial terms, exclusions/dependencies, objection responses, delivery handoff with missing approvals, closed-lost example; no real won deal; handoff to Avery |
| Avery, WES-18 | `dryrun-operations`: stable IDs/stages/owners/dates, duplicate merge history, repeat import with zero new records, literal portable export and round trip, persistent suppression, separate synthetic and zero production counts, review queue and findings |

For each step record the run ID, final status, document key/revision, checks actually executed, review result and next owner. Published prose or a task marked done alone is insufficient. Do not repeat uncertain provider writes: reconcile existing Outlook/HubSpot state and stable IDs first. The earlier mailbox draft and CRM tests remain separate acceptance receipts; these handoffs do not require another mailbox draft or new CRM records unless a specific missing test justifies one.

Keep `send:false`, scheduled heartbeats off, opt-outs intact and unrelated records untouched. WES-20/21/22/23 remain separate acceptance/owner gates. WES-16 is the simulated send-approval test; passing it must never enable a real send. No calendar writes, external contact, new purchases or paid API fallback are authorized.

## Acceptance ledger

| Layer | State from this investigation |
| --- | --- |
| Read-only diagnosis | Typed authentication failure and credential-lifecycle weakness traced; exact provider rejection reason unknown |
| Offline records | Existing 10 unit tests passed; all three regional fixtures validated with zero production records. These checks do not test live runner authentication |
| Host | Origin health passed; capacity recovered to 86% / 63 GiB; isolated SQL restore passed and test resources removed; coordinator released scoped reconnect; off-host backup gap remains |
| Provider | Reconnect and fresh credential acceptance not performed |
| Specialist chain | Scout previously done; the five steps from Quinn through Avery are not accepted by this investigation |
| Owner / outreach | No new authorization; prospect sending remains disabled |

No production release, database migration, task completion, connector write or agent run is implied by merging this documentation.
