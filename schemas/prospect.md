# Portable prospect contract, v1

Each JSON record carries:

| Field | Meaning |
|---|---|
| `id` | Stable internal ID; preserve across imports |
| `company` | Evidence-backed business name; fictional in fixtures |
| `email` | Sourced address, or null when unknown; never guess |
| `territory` | San Diego, Los Angeles or Baja California |
| `synthetic` | Boolean; must be explicit |
| `source_url`, `observed_at` | Source and ISO 8601 evidence date/time |
| `stage` | One of the department stage values |
| `owner`, `next_action`, `next_action_at` | Accountable specialist and dated follow-up |
| `suppressed` | Boolean; suppression wins over stage or approval |
| `outreach_approval` | `pending`, `approved` or `denied` |
| `price` | Null until supported by an approved quote |
| `currency`, `price_approval` | Required when price is provided |

Unknown values are null, not zero or fabricated strings. Contact addresses are deduplicated by trimmed case-insensitive comparison; company matching requires separate domain/name review. Do not merge different people merely because they share a company domain.

The offline validator checks record integrity and whether a record could be eligible for an approved campaign. It does not authorize a campaign. Sending is absent from this repository and disabled during rollout.

HubSpot field IDs and enum values must be discovered from the connected account. Do not assume this portable vocabulary is the provider's API schema. Keep a mapping with each integration release.
