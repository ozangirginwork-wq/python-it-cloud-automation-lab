from types import SimpleNamespace
from unittest.mock import patch
import pytest
from src.event_log_checks import check_recent_event_errors


@pytest.mark.parametrize('hours', [0, -1, 8761, '24; whoami', True])
def test_rejects_invalid_hours_before_powershell(hours):
    with patch('src.event_log_checks.subprocess.run') as run:
        with pytest.raises(ValueError):
            check_recent_event_errors(hours)
        run.assert_not_called()


def test_query_failure_is_not_reported_as_healthy():
    with patch('src.event_log_checks.subprocess.run', return_value=SimpleNamespace(returncode=1, stdout='', stderr='Access denied')):
        result = check_recent_event_errors()
    assert result['status'] == 'FAILED'
    assert result['error_count'] is None


def test_missing_powershell_is_reported():
    with patch('src.event_log_checks.subprocess.run', side_effect=FileNotFoundError('powershell.exe')):
        assert check_recent_event_errors()['status'] == 'FAILED'


@pytest.mark.parametrize('count,status', [('0', 'OK'), ('3', 'WARNING')])
def test_successful_event_count(count, status):
    with patch('src.event_log_checks.subprocess.run', return_value=SimpleNamespace(returncode=0, stdout=count, stderr='')):
        result = check_recent_event_errors()
    assert result['status'] == status
    assert result['error_count'] == int(count)
