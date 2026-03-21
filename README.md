# philiprehberger-portcheck

[![Tests](https://github.com/philiprehberger/py-portcheck/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-portcheck/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-portcheck.svg)](https://pypi.org/project/philiprehberger-portcheck/)
[![License](https://img.shields.io/github/license/philiprehberger/py-portcheck)](LICENSE)

Check if a port is open on a host.

## Installation

```bash
pip install philiprehberger-portcheck
```

## Usage

```python
from philiprehberger_portcheck import is_open, scan, wait_for

# Single port check
is_open("localhost", 8080)                  # True/False
is_open("192.168.1.1", 22, timeout=2.0)    # True/False

# Scan multiple ports
results = scan("localhost", ports=[80, 443, 8080, 5432])
for port, result in results.items():
    if result.is_open:
        print(f"Port {port}: open ({result.service})")

# Scan common ports
results = scan("localhost", ports="common")

# Wait for a port to become available
wait_for("localhost", 5432, timeout=30)
```

## API

| Function / Class | Description |
|------------------|-------------|
| `is_open(host, port, timeout=2.0)` | Check if a TCP port is open |
| `scan(host, ports, timeout=1.0, max_workers=50)` | Scan multiple ports concurrently |
| `wait_for(host, port, timeout=30, interval=1.0)` | Block until port opens or raise `TimeoutError` |
| `PortResult` | Scan result — `.port`, `.is_open`, `.service` |
| `COMMON_PORTS` | List of well-known port numbers (HTTP, SSH, DB, etc.) |


## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## License

MIT
