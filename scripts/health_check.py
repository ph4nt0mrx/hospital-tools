#!/usr/bin/env python3
"""Runs basic connectivity and service health checks on managed endpoints."""
import socket
import subprocess
import json


TIMEOUT = 5
SERVICES = ["W32Time", "WinRM", "Spooler"]


def ping(host):
    try:
        result = subprocess.run(
            ["ping", "-n", "1", "-w", "1000", host],
            capture_output=True, timeout=TIMEOUT
        )
        return result.returncode == 0
    except Exception:
        return False


def check_port(host, port):
    try:
        s = socket.create_connection((host, port), timeout=TIMEOUT)
        s.close()
        return True
    except Exception:
        return False


def check_service(service_name):
    try:
        result = subprocess.run(
            ["sc", "query", service_name],
            capture_output=True, text=True, timeout=TIMEOUT
        )
        return "RUNNING" in result.stdout
    except Exception:
        return False


def run_checks(hostname):
    report = {
        "host": hostname,
        "ping": ping(hostname),
        "rdp": check_port(hostname, 3389),
        "winrm": check_port(hostname, 5985),
        "services": {svc: check_service(svc) for svc in SERVICES},
    }
    return report


if __name__ == "__main__":
    targets = ["CRT-01", "CRT-02", "NRS-01", "NRS-02"]
    for t in targets:
        print(json.dumps(run_checks(t), indent=2))
