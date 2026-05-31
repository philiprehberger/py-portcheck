# philiprehberger-portcheck

[![Tests](https://github.com/philiprehberger/py-portcheck/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-portcheck/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-portcheck.svg)](https://pypi.org/project/philiprehberger-portcheck/)
[![Last updated](https://img.shields.io/github/last-commit/philiprehberger/py-portcheck)](https://github.com/philiprehberger/py-portcheck/commits/main)

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

### Service lookup

```python
from philiprehberger_portcheck import SERVICES, service_name

service_name(443)        # "https"
service_name(22)         # "ssh"
service_name(99999)      # "" (unknown port)

# Read directly from the well-known port map
SERVICES[5432]           # "postgresql"
```

## API

| Function / Class | Description |
|------------------|-------------|
| `is_open(host, port, timeout=2.0)` | Check if a TCP port is open |
| `scan(host, ports, timeout=1.0, max_workers=50)` | Scan multiple ports concurrently |
| `wait_for(host, port, timeout=30, interval=1.0)` | Block until port opens or raise `TimeoutError` |
| `service_name(port)` | Look up the service name for a port (falls back to `socket.getservbyport`) |
| `PortResult` | Scan result — `.port`, `.is_open`, `.service` |
| `SERVICES` | Read-only mapping of well-known port numbers to service names |
| `COMMON_PORTS` | List of well-known port numbers (HTTP, SSH, DB, etc.) |

## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## Support

If you find this project useful:

⭐ [Star the repo](https://github.com/philiprehberger/py-portcheck)

🐛 [Report issues](https://github.com/philiprehberger/py-portcheck/issues?q=is%3Aissue+is%3Aopen+label%3Abug)

💡 [Suggest features](https://github.com/philiprehberger/py-portcheck/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)

❤️ [Sponsor development](https://github.com/sponsors/philiprehberger)

🌐 [All Open Source Projects](https://philiprehberger.com/open-source-packages)

💻 [GitHub Profile](https://github.com/philiprehberger)

🔗 [LinkedIn Profile](https://www.linkedin.com/in/philiprehberger)

## License

[MIT](LICENSE)
