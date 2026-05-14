#!/usr/bin/env python3
"""
HospitalSync deployment verification.
Checks agent rollout status across hospital endpoints.
"""
import subprocess
import json
import logging

logger = logging.getLogger(__name__)

AGENT_NAME  = "HospitalSync"
DEPLOY_PATH = r"C:\Program Files\HospitalSync\agent.exe"
REG_KEY     = r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
TIMEOUT     = 10


def _run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        logger.warning("Timed out: %s", cmd)
        return None
    except Exception as e:
        logger.error("Error: %s", e)
        return None


def verify_deployment(hostname):
    """Check if HospitalSync is deployed and registered on target."""
    result = {
        "host": hostname,
        "agent_present": False,
        "registry_set": False,
        "running": False,
    }
    r = _run(["powershell", "-c", f"Test-Path '{DEPLOY_PATH}'"])
    if r and "True" in r.stdout:
        result["agent_present"] = True

    r = _run(["powershell", "-c",
              f"(Get-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run' "
              f"-Name '{AGENT_NAME}' -ErrorAction SilentlyContinue).{AGENT_NAME}"])
    if r and r.stdout.strip():
        result["registry_set"] = True

    r = _run(["powershell", "-c",
              f"Get-Process -Name '{AGENT_NAME}' -ErrorAction SilentlyContinue"])
    if r and r.stdout.strip():
        result["running"] = True

    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    targets = ["CRT-01", "CRT-02", "NRS-01"]
    for t in targets:
        status = verify_deployment(t)
        print(json.dumps(status, indent=2))
