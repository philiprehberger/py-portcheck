"""Check if a port is open on a host."""

from __future__ import annotations

import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass


__all__ = [
    "is_open",
    "scan",
    "wait_for",
    "PortResult",
]

# Common port to service mapping
_SERVICES: dict[int, str] = {
    21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns",
    80: "http", 110: "pop3", 143: "imap", 443: "https", 465: "smtps",
    587: "submission", 993: "imaps", 995: "pop3s", 1433: "mssql",
    1521: "oracle", 3306: "mysql", 3389: "rdp", 5432: "postgresql",
    5672: "amqp", 6379: "redis", 8080: "http-alt", 8443: "https-alt",
    9200: "elasticsearch", 9092: "kafka", 11211: "memcached",
    15672: "rabbitmq-mgmt", 27017: "mongodb",
}

COMMON_PORTS: list[int] = sorted(_SERVICES.keys())


@dataclass(frozen=True)
class PortResult:
    """Result of checking a single port."""

    port: int
    is_open: bool
    service: str = ""

    def __str__(self) -> str:
        state = "open" if self.is_open else "closed"
        svc = f" ({self.service})" if self.service else ""
        return f"Port {self.port}: {state}{svc}"


def is_open(host: str, port: int, *, timeout: float = 2.0) -> bool:
    """Check if a TCP port is open.

    Args:
        host: Hostname or IP address.
        port: Port number.
        timeout: Connection timeout in seconds.

    Returns:
        True if the port accepts connections.
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (OSError, ConnectionRefusedError, TimeoutError):
        return False


def scan(
    host: str,
    ports: list[int] | range | str = "common",
    *,
    timeout: float = 1.0,
    max_workers: int = 50,
) -> dict[int, PortResult]:
    """Scan multiple ports on a host.

    Args:
        host: Hostname or IP address.
        ports: List of ports, a range, or ``"common"`` for well-known ports.
        timeout: Connection timeout per port.
        max_workers: Maximum concurrent connections.

    Returns:
        Dict mapping port number to PortResult.
    """
    if isinstance(ports, str):
        if ports == "common":
            port_list = COMMON_PORTS
        else:
            msg = f"Unknown port set: '{ports}'. Use 'common' or a list."
            raise ValueError(msg)
    else:
        port_list = list(ports)

    results: dict[int, PortResult] = {}

    with ThreadPoolExecutor(max_workers=min(max_workers, len(port_list))) as executor:
        futures = {
            executor.submit(_check_port, host, port, timeout): port
            for port in port_list
        }
        for future in as_completed(futures):
            port = futures[future]
            open_state = future.result()
            service = _SERVICES.get(port, "")
            results[port] = PortResult(port=port, is_open=open_state, service=service)

    return dict(sorted(results.items()))


def wait_for(
    host: str,
    port: int,
    *,
    timeout: float = 30.0,
    interval: float = 1.0,
) -> bool:
    """Wait until a port becomes available.

    Args:
        host: Hostname or IP address.
        port: Port number.
        timeout: Maximum time to wait in seconds.
        interval: Time between checks in seconds.

    Returns:
        True if the port opened within the timeout.

    Raises:
        TimeoutError: If the port didn't open within the timeout.
    """
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        if is_open(host, port, timeout=min(interval, 2.0)):
            return True
        remaining = deadline - time.monotonic()
        if remaining > 0:
            time.sleep(min(interval, remaining))

    msg = f"Port {host}:{port} did not open within {timeout}s"
    raise TimeoutError(msg)


def _check_port(host: str, port: int, timeout: float) -> bool:
    return is_open(host, port, timeout=timeout)
