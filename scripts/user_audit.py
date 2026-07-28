#!/usr/bin/env python3
"""Audits local user accounts and group memberships on managed endpoints."""
import subprocess
import json
import logging

logger = logging.getLogger(__name__)

PRIVILEGED_GROUPS = ["Administrators", "Remote Desktop Users", "Remote Management Users"]


def list_local_users():
    ps = (
        "Get-LocalUser "
        "| Select-Object Name,Enabled,LastLogon,PasswordLastSet "
        "| ConvertTo-Json -Compress"
    )
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps],
            capture_output=True, text=True, timeout=15
        )
        if r.returncode == 0 and r.stdout.strip():
            return json.loads(r.stdout)
    except Exception as e:
        logger.error("list_local_users: %s", e)
    return []


def list_group_members(group):
    ps = (
        f"Get-LocalGroupMember -Group '{group}' "
        "| Select-Object Name,ObjectClass "
        "| ConvertTo-Json -Compress"
    )
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps],
            capture_output=True, text=True, timeout=15
        )
        if r.returncode == 0 and r.stdout.strip():
            return json.loads(r.stdout)
    except Exception as e:
        logger.error("list_group_members(%s): %s", group, e)
    return []


def audit():
    return {
        "users": list_local_users(),
        "privileged_groups": {
            g: list_group_members(g) for g in PRIVILEGED_GROUPS
        },
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(json.dumps(audit(), indent=2, default=str))
