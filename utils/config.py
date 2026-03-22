#!/usr/bin/env python3
"""Shared config loader for hospital-tools scripts."""
import os
import json
import logging

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "staging_path": r"C:\Staging\Updates",
    "max_age_days": 30,
    "asset_db_url": "https://assets.internal.local/api/v2",
    "targets": ["CRT-01", "CRT-02", "NRS-01", "NRS-02"],
    "log_level": "INFO",
}

_CONFIG_PATHS = [
    os.path.join(os.path.dirname(__file__), "..", "config.json"),
    os.path.expanduser("~/.hospital-tools/config.json"),
    r"C:\ProgramData\HospitalTools\config.json",
]


def load(path=None):
    cfg = dict(DEFAULT_CONFIG)
    search = [path] if path else _CONFIG_PATHS
    for p in search:
        if p and os.path.isfile(p):
            try:
                with open(p) as f:
                    overrides = json.load(f)
                cfg.update(overrides)
                logger.debug("Loaded config from %s", p)
                break
            except Exception as e:
                logger.warning("Could not load config %s: %s", p, e)
    return cfg
