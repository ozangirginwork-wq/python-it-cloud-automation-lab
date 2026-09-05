from src.system_health import collect_system_health, get_status


def test_status_is_ok_below_threshold():
    assert get_status(79.9) == "OK"


def test_status_is_warning_at_threshold():
    assert get_status(80.0) == "WARNING"


def test_system_health_contains_expected_sections():
    health = collect_system_health()

    assert "cpu" in health
    assert "memory" in health
    assert "disk" in health

    assert health["cpu"]["status"] in {"OK", "WARNING"}
    assert health["memory"]["status"] in {"OK", "WARNING"}
    assert health["disk"]["status"] in {"OK", "WARNING"}