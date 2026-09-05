from datetime import datetime
from pathlib import Path
import platform
import socket

import psutil


WARNING_THRESHOLD = 80.0


def get_status(usage_percent):
    """Return a warning when resource usage reaches 80%."""
    if usage_percent >= WARNING_THRESHOLD:
        return "WARNING"
    return "OK"


def collect_system_health():
    """Collect basic health information from the computer."""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage(Path.home().anchor).percent

    return {
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "hostname": socket.gethostname(),
        "operating_system": platform.platform(),
        "cpu": {
            "usage_percent": cpu_usage,
            "status": get_status(cpu_usage),
        },
        "memory": {
            "usage_percent": memory_usage,
            "status": get_status(memory_usage),
        },
        "disk": {
            "usage_percent": disk_usage,
            "status": get_status(disk_usage),
        },
    }