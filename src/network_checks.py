import socket


def check_dns(hostname):
    """Resolve a hostname into an IP address."""
    try:
        ip_address = socket.gethostbyname(hostname)
        return {
            "target": hostname,
            "ip_address": ip_address,
            "status": "OK",
        }
    except socket.gaierror as error:
        return {
            "target": hostname,
            "ip_address": None,
            "status": "FAILED",
            "error": str(error),
        }


def check_tcp_port(hostname, port, timeout=3):
    """Test whether a TCP network service can be reached."""
    try:
        with socket.create_connection((hostname, port), timeout=timeout):
            return {
                "target": hostname,
                "port": port,
                "status": "OK",
            }
    except OSError as error:
        return {
            "target": hostname,
            "port": port,
            "status": "FAILED",
            "error": str(error),
        }


def collect_network_health(target="github.com"):
    """Run DNS and secure web connectivity checks."""
    return {
        "dns": check_dns(target),
        "https": check_tcp_port(target, 443),
    }