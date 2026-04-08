#!/usr/bin/env python3
"""Syncs hardware inventory with asset management DB."""
import csv
import json
import logging
import os
import socket

logger = logging.getLogger(__name__)

ASSET_DB   = "https://assets.internal.local/api/v2"
BATCH_SIZE = 50
INVENTORY  = r"C:\IT\assets\inventory.csv"


def collect_local():
    """Pull basic system info from localhost."""
    return {
        "hostname": socket.gethostname(),
        "os": os.name,
        "cwd": os.getcwd(),
    }


def load_csv(path):
    if not os.path.isfile(path):
        logger.warning("Inventory file not found: %s", path)
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def post_batch(records, endpoint):
    try:
        import urllib.request
        data = json.dumps(records).encode()
        req = urllib.request.Request(
            endpoint, data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception as e:
        logger.error("POST failed: %s", e)
        return False


def sync_inventory(csv_path=INVENTORY, db_url=ASSET_DB):
    records = load_csv(csv_path)
    if not records:
        records = [collect_local()]
    ok = total = 0
    for i in range(0, len(records), BATCH_SIZE):
        batch = records[i:i + BATCH_SIZE]
        if post_batch(batch, db_url):
            ok += len(batch)
        total += len(batch)
    logger.info("Synced %d/%d records", ok, total)
    return ok, total


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sync_inventory()
