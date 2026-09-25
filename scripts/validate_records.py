"""Offline preflight only. No network calls, credentials, or sending capability."""
import argparse
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

TERRITORIES = {"San Diego", "Los Angeles", "Baja California"}
STAGES = {"suppressed", "researched", "qualified", "pending_confirmation",
          "approved_for_outreach", "contacted", "replied", "discovery_scheduled",
          "scoping", "proposal_drafted", "proposal_approved", "won", "lost"}
OWNERS = {"Westy", "Scout", "Quinn", "Harper", "Riley", "Morgan", "Avery"}
APPROVALS = {"pending", "approved", "denied"}


def email_key(value):
    return value.strip().casefold() if isinstance(value, str) else None


def valid_timestamp(value):
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.tzinfo is not None
    except ValueError:
        return False


def valid_source(value):
    if not isinstance(value, str):
        return False
    try:
        parsed = urlparse(value)
        return bool(parsed.scheme == "https" and parsed.hostname
                    and not parsed.username and not parsed.password
                    and not any(c.isspace() for c in value))
    except ValueError:
        return False


def validate(records):
    errors, ids, emails = [], set(), set()
    if not isinstance(records, list):
        return ["input must be a JSON array"]
    for index, r in enumerate(records):
        label = f"record {index + 1}"
        if not isinstance(r, dict):
            errors.append(f"{label}: must be an object")
            continue
        record_id = r.get("id")
        if not isinstance(record_id, str) or not record_id.strip():
            errors.append(f"{label}: missing stable id")
        elif record_id in ids:
            errors.append(f"{label}: duplicate id")
        else:
            ids.add(record_id)
        for field in ("company", "next_action"):
            if not isinstance(r.get(field), str) or not r[field].strip():
                errors.append(f"{label}: missing {field}")
        for field in ("observed_at", "next_action_at"):
            if not valid_timestamp(r.get(field)):
                errors.append(f"{label}: {field} needs an ISO timestamp with timezone")
        for field, allowed in (("territory", TERRITORIES), ("stage", STAGES),
                               ("owner", OWNERS), ("outreach_approval", APPROVALS)):
            if not isinstance(r.get(field), str) or r[field] not in allowed:
                errors.append(f"{label}: invalid {field}")
        for field in ("synthetic", "suppressed"):
            if type(r.get(field)) is not bool:
                errors.append(f"{label}: {field} must be an explicit boolean")
        source = r.get("source_url")
        if not valid_source(source):
            errors.append(f"{label}: missing HTTPS source URL")
        email = email_key(r.get("email"))
        if r.get("email") is not None and (not email or email.count("@") != 1
                or not all(email.split("@")) or any(c.isspace() for c in email)):
            errors.append(f"{label}: invalid email")
        if email:
            if email in emails:
                errors.append(f"{label}: duplicate email")
            emails.add(email)
            domain = email.rsplit("@", 1)[-1]
            reserved = domain in {"example.com", "example.org", "example.net"} or domain.endswith(".example.com")
            if r.get("synthetic") is True and not reserved:
                errors.append(f"{label}: synthetic address must use a reserved example domain")
            if reserved and r.get("synthetic") is not True:
                errors.append(f"{label}: reserved example address must be synthetic")
        if r.get("suppressed") is True and r.get("stage") != "suppressed":
            errors.append(f"{label}: suppressed records cannot remain in an active stage")
        if r.get("stage") == "suppressed" and r.get("suppressed") is not True:
            errors.append(f"{label}: suppressed stage requires suppression flag")
        price = r.get("price")
        if price is not None:
            if type(price) not in (int, float) or price < 0 or price != price or price == float("inf"):
                errors.append(f"{label}: invalid price")
            if r.get("price_approval") != "approved" or r.get("currency") not in {"USD", "MXN"}:
                errors.append(f"{label}: price requires approved quote and explicit currency")
    return errors


def campaign_eligible(record, campaign_enabled=False):
    """Necessary record conditions only; runtime permissions remain separate."""
    return bool(campaign_enabled is True and not validate([record])
                and record["synthetic"] is False and record["suppressed"] is False
                and email_key(record.get("email"))
                and record["outreach_approval"] == "approved"
                and record["stage"] == "approved_for_outreach")


def production_records(records):
    errors = validate(records)
    if errors:
        raise ValueError("; ".join(errors))
    return [r for r in records if r["synthetic"] is False]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    try:
        records = json.loads(args.path.read_text(encoding="utf-8"))
        errors = validate(records)
    except (OSError, ValueError) as exc:
        errors = [str(exc)]
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    print(f"PASS: {len(records)} records; {len(production_records(records))} production records")
