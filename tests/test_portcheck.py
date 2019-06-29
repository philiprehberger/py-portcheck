import pytest
from philiprehberger_portcheck import is_open, scan, wait_for, PortResult, COMMON_PORTS


def test_is_open_closed_port():
    # Port 1 is almost certainly closed
    assert is_open("127.0.0.1", 1, timeout=0.5) is False


def test_is_open_returns_bool():
    result = is_open("127.0.0.1", 65534, timeout=0.5)
    assert isinstance(result, bool)


def test_scan_returns_dict():
    results = scan("127.0.0.1", ports=[1, 2, 3], timeout=0.5)
    assert isinstance(results, dict)
    assert len(results) == 3


def test_scan_port_result():
    results = scan("127.0.0.1", ports=[1], timeout=0.5)
    result = results[1]
    assert isinstance(result, PortResult)
    assert result.port == 1
    assert isinstance(result.is_open, bool)


def test_scan_common_ports():
    results = scan("127.0.0.1", ports="common", timeout=0.2, max_workers=10)
    assert len(results) == len(COMMON_PORTS)


def test_scan_invalid_port_set():
    with pytest.raises(ValueError):
        scan("127.0.0.1", ports="invalid")


def test_port_result_str():
    result = PortResult(port=80, is_open=True, service="http")
    text = str(result)
    assert "80" in text
    assert "open" in text
    assert "http" in text


def test_port_result_closed():
    result = PortResult(port=443, is_open=False, service="https")
    text = str(result)
    assert "closed" in text


def test_wait_for_timeout():
    with pytest.raises(TimeoutError):
        wait_for("127.0.0.1", 1, timeout=0.5, interval=0.1)


def test_common_ports_sorted():
    assert COMMON_PORTS == sorted(COMMON_PORTS)


def test_scan_with_range():
    results = scan("127.0.0.1", ports=range(60000, 60003), timeout=0.3)
    assert len(results) == 3
