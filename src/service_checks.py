import psutil


SERVICES_TO_CHECK = {
    "Windows Event Log": "EventLog",
    "DNS Client": "Dnscache",
    "Microsoft Defender": "WinDefend",
}


def check_service(display_name, service_name):
    """Check whether a Windows service is running."""
    try:
        service = psutil.win_service_get(service_name)
        current_status = service.status()

        return {
            "display_name": display_name,
            "service_name": service_name,
            "current_status": current_status,
            "status": "OK" if current_status == "running" else "WARNING",
        }

    except psutil.NoSuchProcess:
        return {
            "display_name": display_name,
            "service_name": service_name,
            "current_status": "not found",
            "status": "FAILED",
        }

    except psutil.AccessDenied:
        return {
            "display_name": display_name,
            "service_name": service_name,
            "current_status": "access denied",
            "status": "FAILED",
        }


def collect_service_health():
    """Check all important Windows services."""
    return [
        check_service(display_name, service_name)
        for display_name, service_name in SERVICES_TO_CHECK.items()
    ]