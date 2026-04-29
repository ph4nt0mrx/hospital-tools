#!/usr/bin/env python3
"""Collects Windows event logs from endpoints and writes them to a central share."""
import os
import subprocess
import datetime
import json
import logging

logger = logging.getLogger(__name__)

LOG_SOURCES = ["System", "Application", "Security"]
OUTPUT_DIR  = r"\\fileserver\IT\logs"
MAX_ENTRIES = 500


def collect_event_log(source, max_entries=MAX_ENTRIES):
    cmd = [
        "powershell", "-NoProfile", "-Command",
        f"Get-EventLog -LogName '{source}' -Newest {max_entries} "
        f"| Select-Object TimeGenerated,EntryType,Source,EventID,Message "
        f"| ConvertTo-Json -Compress"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception as e:
        logger.error("Failed to collect %s: %s", source, e)
    return []


def collect_all(output_dir=OUTPUT_DIR):
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    hostname = os.environ.get("COMPUTERNAME", "unknown")
    os.makedirs(output_dir, exist_ok=True)
    results = {}
    for src in LOG_SOURCES:
        logger.info("Collecting %s ...", src)
        entries = collect_event_log(src)
        results[src] = len(entries)
        out = os.path.join(output_dir, f"{hostname}_{src}_{ts}.json")
        with open(out, "w") as f:
            json.dump(entries, f)
        logger.info("  wrote %d entries → %s", len(entries), out)
    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    collect_all()
