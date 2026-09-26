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

This proves a working authenticated Quinn turn and reviewed prepared qualification output. The authoritative rubric was subsequently published as v2.2.0 revision 7, and Quinn finalized the artifact as recorded below. WES-14 requires a scored demonstration and handoff; it does not require authoritative CSV/history writes before Harper. Those unapplied changes remain part of Avery's WES-18 acceptance. The four-record fixture has no positively evidenced disqualification; the illustrative example is not a fifth record. WES-39 must supply the actual synthetic disqualifier before Avery's lost-route and round-trip acceptance.

### Publication editor incident and exact restoration

The current task interface exposes documents read-only. Frankie explicitly approved temporarily enabling the instance-wide **Classic Task Interface**, publishing the exact reviewed rubric, and restoring the original view. The approved source remained `rubric-v220-body` revision 2 on WES-14, SHA-256 `741a91b0fa7fcea190c4b613440111e0c070cc5c92ee606d0de0995f9a1611c6` (41,548 UTF-8 bytes).

At **03:53:12.503 UTC**, opening **Edit document** on the target WES-12 rubric automatically created revision 5 before any text was entered. Its title remained v2.1.0 and its format remained Markdown, but the rich editor reserialized 29,590 bytes into 46,142 bytes. The editor's initial nonempty `onChange` reached the document's 900 ms autosave. This was an unintended write, not the requested v2.2.0 publication.

Both 270-line bodies were preserved and compared. They are exactly equal after normalizing only table padding/separator widths, horizontal-rule spelling, and Markdown escapes before `=` and `~`; wording, numbers, links and order are unchanged. Revision 4 has SHA-256 `056708a9fef893106afb870bed7b96cbd635feb4aa8f8126dbb98f3808fc19ce`; revision 5 has `d62e7ef7e69291a4057c3ef1ac6ab2ada662fea8f3c68df0860934d858c7e8a7`.

After that comparison and coordinator review, the supported revision-history **Restore this revision** action restored revision 4 once, without mounting the editor. At **03:56:47.121 UTC**, it created revision 6 (`d9e95740-1092-462a-baf8-4de46fc84b0b`) with the exact revision-4 body hash, original v2.1.0 title and Markdown format. Both earlier revisions remain in append-only history. **Classic Task Interface was restored OFF at 03:57:22.835 UTC.** The audit showed no additional issue status, score-history or other-document changes, no new agent run, and the same five deferred Westy requests. An unrelated tool-connection webhook was recorded during the window and was not attributed to this operation.

The UI attempt left exact v2.2.0 publication blocked. The installed rich editor has no normal raw-source toggle; its raw textarea is an error fallback. A proposed Quinn native document PUT was rejected during source review without starting a run: `PUT /api/issues/:id/documents/:key` calls the assignee mutation guard, and Quinn cannot edit Westy's WES-12 document without an applicable management override. Do not change assignment, expand grants, induce an editor error, extract browser credentials or write the database to bypass that boundary. A supported board CLI exists, but no existing board credential was found in the inspected runtime/default local stores. The separate owner-approved path below resolved publication.

### Exact publication and temporary-access cleanup

Frankie explicitly approved creating temporary CLI access for his existing Paperclip account, making one exact rubric publication, verifying it, and immediately revoking/removing the credential, including cleanup on failure. The approval disclosed that the key is account-wide rather than document-scoped and has a default 30-day lifetime. The normal installed CLI login used a dedicated owner-only temporary auth store. Its identity endpoint verified the existing owner and expected company before publication; no browser session credential was extracted.

At **04:09:00 UTC**, after confirming zero active runs and unchanged source/target revisions, one supported document PUT used revision 6 as its optimistic-concurrency base. An independent GET confirmed **v2.2.0 revision 7** (`998d72e2-93a7-41fa-87bc-5f6e5285265e`), the intended title, Markdown format, **41,548 UTF-8 bytes**, and SHA-256 `741a91b0fa7fcea190c4b613440111e0c070cc5c92ee606d0de0995f9a1611c6`, exactly matching the reviewed WES-14 source. The restored chat interface also displayed the version and revision.

The temporary key was revoked immediately at **04:09:00.230 UTC**. A subsequent identity request using that same key returned **401**, and both the runtime auth/log directory and local approval-link directory were removed. Cleanup ran in a `finally` block. Audit events were key creation, the single document update, and key revocation. No agent run, task status, other document, score-history or deferred-wake change accompanied publication; Classic Task Interface stayed off. No token or authorization code is part of this receipt.

The eventual record handoff has separate writer boundaries. Synthetic records and their history belong in WES-13's `synthetic-prospects` document, which is assigned to Scout; WES-24's `stage-history` holds production events and still has zero rows. Its rules explicitly keep synthetic events on WES-13. Avery alone writes `id-counters`, currently revision 3. Field-level authorship and Paperclip's document-assignee permission are separate boundaries: Quinn's prepared score blocks do not prove an authoritative record/history write. The live dependency graph already orders **WES-37 → WES-39 → WES-18**; WES-39's prose saying it follows WES-18 is stale. Preserve that graph and review the exact writer/counter/history sequence before applying records. No new history ID or historical timestamp is justified by a prepared score block alone.

### Final qualification artifact and answered-question replay

Bounded finalization run `c5c698c5-c5cb-47c9-a8c8-7adadf5387f6` succeeded at **04:27:59.279 UTC**. It published `dryrun-qualification` revision 4 (`26e403a0-f4a3-4d1e-ac17-766a7c2ea5d5`), 63,276 UTF-8 bytes, SHA-256 `f2d0a7e478685d0f48ec35b49b5b97175914d49f53ed1358a3b6b02960db0f37`. Independent worker and coordinator review covered all 11 changed regions. All seven score blocks are byte-identical to revision 3; per-dimension evidence, citations, duplicate reasoning and arithmetic are preserved. The changes identify the published rubric, separate prepared decisions from actual record writes, and explicitly retain the illustrative disqualification limitation and fifth-fixture sequence.

Handoff comment `7baebcc2-b071-4d9d-ace7-7c79fcedf7b7` identifies **zero eligible first-touch recipients**. Harper must still produce the required English and Spanish examples, held as synthetic drafts. PRS-000002 has a named contact but no named-person route; its role mailbox does not establish eligibility. PRS-000003 remains pending confirmation for on-site coverage, Spanish service delivery and Mexican-entity contracting. The finalization wrote only the owned qualification artifact and one handoff comment; it made no connector calls or record/history/counter changes. The document meets WES-14's six demonstration requirements, with actual lost-route acceptance still reserved for the later fifth record and Avery.

At **04:28:12.436 UTC**, Paperclip started an unexpected follow-on, `c2f7edb6-c33b-4a2e-bc8a-e612d651f433`. It was stopped through the UI and **cancelled at 04:28:33.772 UTC**. Unlike the earlier deferred-wake promotion, this was a fresh system `issue_continuation_needed` wake for answered question `fe51fca2-25de-4a72-a26c-519286cc26a2`, originally resolved September 25 at 18:22:09 UTC. The installed recovery service requires a successful run whose context names that exact interaction; the successful comment-triggered finalization has no interaction ID and did not satisfy that check.

The stopped follow-on made no deliverable, comment, status or connector changes. Its sole document revision was application-generated `continuation-summary` revision 9. Its cancellation is attributed to a user, which the installed recovery service exempts while it remains the latest run. Marking an accepted WES-14 done also removes it from the recovery candidate statuses. At this checkpoint there are zero queued/running runs and the same five historical Westy deferred requests. No database edits or expanded permissions were used to suppress recovery. WES-14 remains in progress while the Harper prerequisite below is held; after review, Harper must receive one bounded native dependency wake, not an additional manual start.

### Harper prerequisite and confirmed launch-size failure

Before editing WES-15 or completing WES-14, the full task history exposed an existing prerequisite: apply `v06-prerender-spec` revision 17 (`7646daa1-e355-4abd-b713-d0143d335060`, 71,780 bytes) before rendering the synthetic drafts. WES-6 remains assigned to Harper and done, with `outreach-templates` revision 9 (`659c69b8-70a0-4bac-abd3-5b7866900fa1`, 79,488 bytes) and `claim-ledger` revision 6 (`f8f0e6b7-96df-4aae-9618-c36d8cf836c6`, 43,105 bytes). The ledger title is null; its specified last-good title must be restored with the full publication, not through an extra title-only revision. The native same-assignee writer path is available without a new board credential or reassignment.

The staged update closes the approved W-16/W-17 decisions, reconciles marker classification checks and stale live revision references, advances the template to v0.6, and binds the ledger to the independently re-read new template revision. All twelve message bodies must remain byte-identical, commercial unknowns remain unresolved, both prepared bodies must contain zero unfilled `<<` slots, and the exact full-body diffs require review before publication. Only then can Harper produce the original six WES-15 demonstrations. The earlier proposed restriction to writing only `dryrun-outreach` was withdrawn before any description or status edit because it would omit this prerequisite.

Harper's latest historical run, `f5989d7e-6f99-4e8d-a2f6-666ca55d8910`, failed on September 25 at 16:28:27 UTC with `acpx_session_init_failed` / `spawn E2BIG`, before a provider turn. Read-only inspection reproduced the failure mechanism: the installed wake serializer emits **145,794 bytes** for that run's payload, and starting harmless `/bin/true` with a synthetic environment string of the same size returns **E2BIG**. No credential or actual business payload was sent to that probe. The envelope contains full comment history plus a resume delta, and the ACP engine exports it as one unbounded `PAPERCLIP_WAKE_PAYLOAD_JSON` value. A size model removing the old comment batch and delta yields 124,380 bytes, but that is not acceptance evidence for the next run. The full history is reconstructed at dispatch; a fresh session cannot be relied on to cure the transport defect.

The pre-repair image was `ghcr.io/paperclipai/paperclip@sha256:a02ac35ac41df911af477422ea0e781cf41d2b2c600c66f0a5ac9d8c63f52c2c`, OCI version `2026.916.1`, upstream source revision `d554c4789ed3930f8a53ac9fdf6503b3187097da` in `paperclipai/paperclip`. The local `Seckcey/paperclip` repository holds operations documentation, not this application source. No runtime code, configuration, task description, template or ledger was changed during the investigation.

The authorized source repair is committed as `bbd1ed5bee21a4fd1eccd1c6cc474679100ad2ad` on isolated branch `fix/bounded-wake-payload`, based on the exact installed upstream revision. The shared ACP engine already delivers the authorized wake through its prompt. The repair limits only the optional `PAPERCLIP_WAKE_PAYLOAD_JSON` environment copy to **16 KiB of UTF-8 JSON** and prevents configured environment values from restoring an oversized runtime copy. Larger wakes retain the existing full fresh-session prompt or checked resumed-session delta, with an explicit transport note and unchanged source-trust boundaries. No task history is deleted or truncated, no file protocol is added, and legacy non-ACP adapters are unchanged. Repository and installed ACP/Claude consumer inspection found no machine consumer that requires this optional environment copy; the agent skill explicitly handles it only when present.

All **185 ACP execution tests passed** in a task-owned Coastline container, including seven new cases for exact byte boundaries, Unicode, configured-value override, a **145,794-byte** synthetic wake with successful child spawn on local and remote paths, full oldest/latest history and untrusted-evidence labels, and a retained-session delta. The adapter typecheck and build also passed. The final candidate image also passed all 185 tests using its own runtime files, and its production TypeScript loader resolved and imported the exact patched files. Full repository typecheck and build were attempted but the pinned image lacks `cargo` and `cc` for unrelated packages; the broad suite was stopped incomplete and is not reported as passing. The [merged platform patch and recipe](https://github.com/Seckcey/paperclip/pull/2) build immutable image `sha256:542dc73eb7376cb89ca43c0c1276e0bebd0009ece797d3453a05b835d4c50d60` containing only the two changed runtime files over the pinned base, with the original digest retained for rollback and no database migration. The image was deployed and verified at **05:13:41 UTC** after coordinator release handoff. Only the app was replaced, using a private image-only Compose override, `--no-deps` and `--pull never`. Its running image ID and both runtime source hashes match the tested candidate; loopback and public health both report `ok`. The database container identity, image, start time and mounts are unchanged, as are the application mounts. Schema remains 278 migrations with fingerprint `f65fded17cd93b69fe5fc8e749e3e7d4`. There are zero active/queued runs and the same five historical Westy deferred requests. The 04:16:11 SQL backup (8,247,407 bytes) passed gzip verification; the earlier isolated restore is the recovery baseline. The original image digest remains available for app-only rollback. All task test containers/volumes are absent. **Runner deployment is complete; WES-6 publication and WES-15 workflow acceptance are still pending**, and WES-14/Harper remain held while the full prepared template/ledger edits are reviewed. No prospect sending, credentials, grant or record/history change was part of the release.

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
| Specialist chain | Quinn's final qualification revision 4 and handoff passed independent review; WES-12 v2.2.0 revision 7 published exactly and temporary access revoked. The E2BIG runner repair is deployed and healthy; WES-14 completion and Harper's workflow acceptance remain held for the staged v0.6 template prerequisite. Actual record/history writes remain later acceptance work. Both unexpected follow-ons were stopped without deliverable drift |
| Owner / outreach | No new authorization; prospect sending remains disabled |

No production release, database migration, task completion, connector write or agent run is implied by merging this documentation.
