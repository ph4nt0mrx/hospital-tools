#!/usr/bin/env python3
"""Cleanup old temp files from deployment staging areas."""
import os
import glob
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

STAGING = r"C:\Staging\Updates"
MAX_AGE_DAYS = 30
EXTENSIONS = ["*.tmp", "*.bak", "*.old"]


def cleanup(staging_path=STAGING, max_age_days=MAX_AGE_DAYS, dry_run=False):
    cutoff = time.time() - (max_age_days * 86400)
    removed = 0
    errors = 0
    for ext in EXTENSIONS:
        for f in glob.glob(os.path.join(staging_path, ext)):
            try:
                if os.path.getmtime(f) < cutoff:
                    if not dry_run:
                        os.remove(f)
                    logger.info("Removed: %s", f)
                    removed += 1
            except OSError as e:
                logger.warning("Could not remove %s: %s", f, e)
                errors += 1
    logger.info("Done. Removed: %d, Errors: %d", removed, errors)
    return removed, errors


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Clean up staging temp files")
    parser.add_argument("--path", default=STAGING)
    parser.add_argument("--days", type=int, default=MAX_AGE_DAYS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    cleanup(args.path, args.days, args.dry_run)
