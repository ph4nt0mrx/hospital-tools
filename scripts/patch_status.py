#!/usr/bin/env python3
"""Queries Windows Update patch status on managed endpoints via WMI."""
import subprocess
import json
import logging
import datetime

logger = logging.getLogger(__name__)


def get_installed_patches(limit=20):
    ps = (
        "Get-HotFix "
        "| Sort-Object InstalledOn -Descending "
        f"| Select-Object -First {limit} HotFixID,InstalledOn,Description "
        "| ConvertTo-Json -Compress"
    )
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps],
            capture_output=True, text=True, timeout=30
        )
        if r.returncode == 0 and r.stdout.strip():
            return json.loads(r.stdout)
    except Exception as e:
        logger.error("get_installed_patches failed: %s", e)
    return []


def get_pending_updates():
    ps = (
        "$s = New-Object -ComObject Microsoft.Update.Session; "
        "$searcher = $s.CreateUpdateSearcher(); "
        "$result = $searcher.Search('IsInstalled=0 and Type=Software'); "
        "$result.Updates | Select-Object Title,MsrcSeverity "
        "| ConvertTo-Json -Compress"
    )
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps],
            capture_output=True, text=True, timeout=60
        )
        if r.returncode == 0 and r.stdout.strip():
            return json.loads(r.stdout)
    except Exception as e:
        logger.error("get_pending_updates failed: %s", e)
    return []


def patch_report():
    return {
        "generated": datetime.datetime.utcnow().isoformat() + "Z",
        "installed": get_installed_patches(),
        "pending": get_pending_updates(),
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(json.dumps(patch_report(), indent=2, default=str))
