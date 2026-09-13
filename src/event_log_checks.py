import subprocess


def check_recent_event_errors(hours=24):
    """Count Windows application errors from the specified period."""
    if type(hours) is not int or not 1 <= hours <= 8760:
        raise ValueError("hours must be an integer from 1 to 8760")

    powershell_command = f"""
    $ErrorActionPreference = 'Stop'
    try {{
    $StartTime = (Get-Date).AddHours(-{hours})
    $Events = Get-WinEvent -FilterHashtable @{{
        LogName='Application'
        StartTime=$StartTime
        Level=1,2
    }} -ErrorAction Stop
    @($Events).Count
    }} catch {{
        if ($_.FullyQualifiedErrorId -like 'NoMatchingEventsFound*') {{
            Write-Output 0
        }} else {{
            [Console]::Error.WriteLine($_.Exception.Message)
            exit 1
        }}
    }}
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

        count_text = result.stdout.strip()
        if not count_text.isascii() or not count_text.isdecimal():
            raise ValueError("PowerShell did not return a non-negative event count")
        error_count = int(count_text)

        return {
            "log_name": "Application",
            "lookback_hours": hours,
            "error_count": error_count,
            "status": "OK" if error_count == 0 else "WARNING",
        }

    except (subprocess.TimeoutExpired, ValueError, OSError) as error:
        return {
            "log_name": "Application",
            "lookback_hours": hours,
            "error_count": None,
            "status": "FAILED",
            "error": str(error),
        }