import subprocess


def check_recent_event_errors(hours=24):
    """Count Windows application errors from the specified period."""
    powershell_command = f"""
    $StartTime = (Get-Date).AddHours(-{hours})
    $Events = Get-WinEvent -FilterHashtable @{{
        LogName='Application'
        StartTime=$StartTime
        Level=1,2
    }} -ErrorAction SilentlyContinue
    @($Events).Count
    """

    try:
        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                powershell_command,
            ],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )

        if result.returncode != 0:
            return {
                "log_name": "Application",
                "lookback_hours": hours,
                "error_count": None,
                "status": "FAILED",
                "error": result.stderr.strip(),
            }

        error_count = int(result.stdout.strip() or 0)

        return {
            "log_name": "Application",
            "lookback_hours": hours,
            "error_count": error_count,
            "status": "OK" if error_count == 0 else "WARNING",
        }

    except (subprocess.TimeoutExpired, ValueError) as error:
        return {
            "log_name": "Application",
            "lookback_hours": hours,
            "error_count": None,
            "status": "FAILED",
            "error": str(error),
        }