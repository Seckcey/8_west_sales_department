# Outlook connector acceptance and repair

## Connection format

Paperclip's Zapier form expects the complete generated URL, including its token. In Zapier's credentials dialog this is **Option 2: URL with token — Copy full URL**. Option 1 provides a URL and a separate authorization header, so its URL alone is insufficient for this form. Keep the complete URL out of chat, logs and this repository.

## Personal credential defect

On the deployed Paperclip revision `d554c4789ed3930f8a53ac9fdf6503b3187097da`, setup saved a non-OAuth Zapier URL as a company-scoped encrypted secret while attaching it to a personal grant. Discovery succeeded, but an agent call failed before reaching Microsoft with `grant_credential_invalid`.

Verified in the deployed source: `connectGalleryApp` creates the URL secret with company scope; the agent gateway's `resolveGrantSecretValue` requires a user-scoped value with matching owner and a user-secret definition. This is separate from Microsoft consent or shared mailbox delegation.

## Scoped repair applied

A guarded, transactional maintenance repair created an owner-specific secret definition/value/declaration and updated only the existing personal grant's secret reference. The encrypted value was copied inside the database; no plaintext was exported or rotated. The original encrypted reference remains for Paperclip's existing discovery path. The agent audience, tool permissions and runtime image were preserved.

The transaction was first tested and rolled back, then committed after its scope and declaration checks passed. Audit action: `tool_connection.personal_credential_repaired`, reason `owner_scoped_secret_added`. Its private audit details retain the previous grant reference and new record IDs for operator rollback. They contain no token.

After the repair, a real fixed sales-inbox lookup as Westy returned HTTP 200. This proves the saved token, personal grant and delegated inbox read work together.

This is a repair of this saved connection, not an upstream Paperclip code fix. Reconnection, credential rotation or a Paperclip upgrade requires a fresh agent test. Do not copy credentials into documentation or replay database edits against a different connection. An operator can restore the old grant reference from the audit record to roll back, which restores the original nonworking authorization state.

## Action limits

Only Westy, Harper and Riley have the mail connection. Enabled business actions are the fixed sales-inbox GET, draft email and draft reply. Two read-only schema helpers remain available. The automatically advertised generic mutating request action and configuration-link helper are off. No sending, deletion or calendar action is enabled.

The native draft tool expects recipient arrays. Paperclip's current test form submitted its recipient text field as a string, which the provider rejected before any draft was created. Do not treat that UI validation failure as evidence of an invalid token. Agent calls must follow the actual tool schema.

## Draft acceptance

On September 25 at 12:26 UTC, Harper created exactly one synthetic draft through the approved Paperclip gateway. The provider returned `isDraft: true`, a draft identifier, parent-folder identifier and Outlook link, with `qa-sd@example.com` as the sole recipient. Nothing was sent. Private provider identifiers remain in WES-25 rather than this public repository.

The action is configured for `sales@8westit.com`. The creation response returned null `from` and `sender` fields. Root then opened that shared mailbox in Outlook and verified its Drafts folder contained exactly one message with the expected synthetic subject, recipient and body; Sent Items showed zero items. Mailbox placement and unsent state are therefore verified separately from the creation response. The test draft remains in place.

Outlook resolves `sales@8westit.com` to a mailbox whose displayed primary address is `sales@8westventures.com`. This does not prevent the verified shared-mailbox read/draft workflow. Before enabling any future sending, verify the intended From alias; the null provider fields do not establish the outgoing sender identity.

Three agent attempts failed with `acpx_turn_failed` before reaching Outlook after loading the deferred tool. The successful attempt used Paperclip's existing HTTP tool gateway under Harper's own temporary session and the same connection grants. This was not a direct provider call or a permission bypass. The deferred-tool failure and test-form array handling remain upstream issues; the supported gateway route is the verified working path.
