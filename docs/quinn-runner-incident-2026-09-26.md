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
5. Resume exactly one bounded, fresh Quinn run against WES-14, using server-enforced idempotency where the supported surface provides it, and no scheduled heartbeat. A task-message correlation marker is not an idempotency key; reconcile the actual wake/run before retrying. Inventory deferred requests as well as active runs first. Preserve the current subscription/provider, no-send restrictions and existing documents. Stop after one authentication failure rather than blindly retrying. If needed, collect a bounded protected provider trace, retaining only sanitized failure category/status in this repository.

The reconnect path is verified from `ManagedAiConnectionDetails.tsx`, `AiConnectionAccountControls.tsx`, `AiConnectionCredentialStep.tsx`, `useLocalAiLogin.ts`, and the installed local-login routes/services. It was executed successfully on September 26, as recorded below. Opening the reconnect flow itself creates a login attempt; it is not a read-only status check.

A fresh local sign-in may restore a limited work window, but it still imports only the access token in this installed version. It does not repair refresh persistence or prove durable unattended operation. A permanent upstream credential-lifecycle repair or a different officially supported subscription sign-in method needs separate source review, isolated validation and an authorized release. Never copy another application's credentials or silently change the funding source.

### Reconnect receipt, September 26

The owner completed the isolated Claude CLI sign-in in the existing application container. The CLI reported a successful first-party Claude Max login, and Paperclip detected the completed sign-in. At **03:23:08 UTC**, the existing connection's **Connect** action succeeded and its permissions page showed **Connected**. The deployed importer calls `fetchClaudeQuota` before returning the credential; successful import therefore provides provider acceptance at that time, beyond merely observing a signed-in browser.

The same connection, personal owner, active user grant, secret record and Anthropic/subscription default remained in place. The credential record advanced from version **1 to 2**. The permissions remained **Just me**, **Any agent**, and **Your default**; no new connection, paid API method or grant expansion was introduced. No credential value or authorization code belongs in this receipt. Saved health is `ok`, but its health-check timestamps remain null and are not independent acceptance evidence.

At 03:22:56 UTC, Coastline had 63 GiB free (86% used), about 4 GiB available RAM, running app/database containers with no OOM flags, and no queued/running agent jobs. All seven agent identities were preserved. The coordinator then released one bounded WES-14 recovery run, keeping scheduled heartbeats off, `send:false` and downstream runs held for review.

Run `57fa318e-a16c-4cb7-912d-c1e66360f8ee` started at 03:25:54 UTC from one authenticated task message identified as `quinn-reconnect-20260926-01` and **succeeded at 03:38:17 UTC**. Its prior session was null and its existing limit was 40 turns. The wakeup's database idempotency key was null; the message marker is a correlation identifier, not a claim of server-enforced idempotency. Reconcile the actual run before any retry.

It published `dryrun-qualification` revision 3 (SHA-256 `27a942084b00…c7819c15`), `rubric-v220-body` revision 2 (`741a91b0fa7f…9a1611c6`), and `recovery-evidence-receipt` revision 1. The ruling stayed at revision 1. Independent review reproduced the three scored records: `PRS-000001` remains `UNSCORED` with confidence 30; `PRS-000002` remains capped `B` at fit/confidence 80/60; `PRS-000003` remains `B` at 57/65. All four new score blocks, including the explicitly illustrative disqualification, fit the 200-character limit (84/97/86/62 characters). All six duplicate comparisons produce exactly one collision, `PRS-000002` with `PRS-000004`; the S1 survivor is `PRS-000002`, it gains no previously unknown field value, and all three scored records retain their superseded blocks.

This proves a working authenticated Quinn turn and reviewed prepared qualification output. It does **not** complete WES-14: authoritative `qualification-rubric` on WES-12 remains v2.1.0, restored byte-for-byte from revision 4 into revision 6 after the editor incident below. Publication of the reviewed v2.2.0 body and score-history writes remain pending. The four-record fixture has no positively evidenced disqualification; the illustrative example is not a fifth record. WES-39 must supply the actual synthetic disqualifier before Avery's lost-route and round-trip acceptance. WES-15 through WES-18 remain held.

### Publication editor incident and exact restoration

The current task interface exposes documents read-only. Frankie explicitly approved temporarily enabling the instance-wide **Classic Task Interface**, publishing the exact reviewed rubric, and restoring the original view. The approved source remained `rubric-v220-body` revision 2 on WES-14, SHA-256 `741a91b0fa7fcea190c4b613440111e0c070cc5c92ee606d0de0995f9a1611c6` (41,548 UTF-8 bytes).

At **03:53:12.503 UTC**, opening **Edit document** on the target WES-12 rubric automatically created revision 5 before any text was entered. Its title remained v2.1.0 and its format remained Markdown, but the rich editor reserialized 29,590 bytes into 46,142 bytes. The editor's initial nonempty `onChange` reached the document's 900 ms autosave. This was an unintended write, not the requested v2.2.0 publication.

Both 270-line bodies were preserved and compared. They are exactly equal after normalizing only table padding/separator widths, horizontal-rule spelling, and Markdown escapes before `=` and `~`; wording, numbers, links and order are unchanged. Revision 4 has SHA-256 `056708a9fef893106afb870bed7b96cbd635feb4aa8f8126dbb98f3808fc19ce`; revision 5 has `d62e7ef7e69291a4057c3ef1ac6ab2ada662fea8f3c68df0860934d858c7e8a7`.

After that comparison and coordinator review, the supported revision-history **Restore this revision** action restored revision 4 once, without mounting the editor. At **03:56:47.121 UTC**, it created revision 6 (`d9e95740-1092-462a-baf8-4de46fc84b0b`) with the exact revision-4 body hash, original v2.1.0 title and Markdown format. Both earlier revisions remain in append-only history. **Classic Task Interface was restored OFF at 03:57:22.835 UTC.** The audit showed no additional issue status, score-history or other-document changes, no new agent run, and the same five deferred Westy requests. An unrelated tool-connection webhook was recorded during the window and was not attributed to this operation.

Exact v2.2.0 publication remains blocked. The installed rich editor has no normal raw-source toggle; its raw textarea is an error fallback. A proposed Quinn native document PUT was rejected during source review without starting a run: `PUT /api/issues/:id/documents/:key` calls the assignee mutation guard, and Quinn cannot edit Westy's WES-12 document without an applicable management override. Do not change assignment, expand grants, induce an editor error, extract browser credentials or write the database to bypass that boundary. A supported board CLI exists, but no existing board credential was found in the inspected runtime/default local stores; no new token was created. Review a supported owner/admin publication mechanism separately before advancing the chain.

### Historical wakeup discovered after recovery

Paperclip immediately promoted an older deferred request after the successful run. Run `48a8f82e-4612-4f76-a4fc-84e1a78830f5` started at 03:38:17.933 UTC from a request originally made on September 25 at 18:23:46.924 UTC, with reason `issue_execution_promoted`. No second recovery request was submitted. It was stopped through the task UI and recorded **cancelled at 03:39:14.949 UTC**.

The cancelled run changed none of the deliverables above. Its only document revision was the application's generated `continuation-summary` revision 7, which correctly records operator cancellation; its only comment says `cancelled`. Both recovery runs have no recorded connector invocation. The prior successful receipt remains authoritative for completed work; the latest generated continuation summary alone hides that success.

A fresh check found zero queued/running jobs. Five other historical Westy requests remain `deferred_issue_execution`: three target WES-2, and one each targets WES-3 and WES-4. They are preserved pending intent review, not cancelled merely because they are old or their target is done. Harper/WES-15 has no queued, claimed or deferred request at this checkpoint. **Before a bounded retry, inventory deferred requests as well as queued/running jobs**; disabled scheduled heartbeats do not prevent an old deferred request from being promoted.

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
| Provider | Existing subscription reconnected at 03:23:08 UTC; provider import validation and a subsequent Quinn turn succeeded. Durable automatic refresh remains unresolved |
| Specialist chain | Quinn's recovery turn and prepared score checks passed; WES-12 publication/score history and later handoffs remain pending. Unexpected historical follow-on run was cancelled without deliverable drift |
| Owner / outreach | No new authorization; prospect sending remains disabled |

No production release, database migration, task completion, connector write or agent run is implied by merging this documentation.
