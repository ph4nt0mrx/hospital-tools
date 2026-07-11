# hospital-tools

Small collection of IT deployment utilities for hospital endpoint management.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/cleanup.py` | Remove stale temp files from staging areas |
| `scripts/health_check.py` | Connectivity and service health checks |
| `scripts/inventory_sync.py` | Sync hardware inventory to asset DB |
| `scripts/log_collector.py` | Collect Windows event logs to central share |
| `scripts/patch_status.py` | Query installed and pending Windows patches |

## Deploy

See `deploy/agent_updater.py` for the HospitalSync rollout verification step.

## Usage

```bash
pip install -r requirements.txt

# Run health checks
python scripts/health_check.py CRT-01 CRT-02 --json

# Collect logs
python scripts/log_collector.py

# Check patch status
python scripts/patch_status.py

# Sync inventory
python scripts/inventory_sync.py
```

## Config

Optional `config.json` in the repo root overrides defaults (see `utils/config.py`).
