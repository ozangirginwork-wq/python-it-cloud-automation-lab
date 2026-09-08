import argparse

from src.event_log_checks import check_recent_event_errors
from src.network_checks import collect_network_health
from src.reporting import save_html_report, save_json_report
from src.service_checks import collect_service_health
from src.system_health import collect_system_health


def parse_arguments():
    """Read options supplied by the user."""
    parser = argparse.ArgumentParser(
        description="Run Windows IT operations health checks."
    )

    parser.add_argument(
        "--target",
        default="github.com",
        help="Hostname used for DNS and HTTPS tests.",
    )

    parser.add_argument(
        "--event-hours",
        type=int,
        default=24,
        help="Number of hours to examine in the Windows event log.",
    )

    arguments = parser.parse_args()
    if not 1 <= arguments.event_hours <= 8760:
        parser.error("--event-hours must be between 1 and 8760")
    return arguments


def display_metric(name, details):
    """Display one system measurement."""
    usage = details["usage_percent"]
    status = details["status"]
    print(f"{name:<8}: {usage:>5.1f}%  [{status}]")


def main():
    """Run, display and save all health checks."""
    arguments = parse_arguments()

    health = collect_system_health()
    network = collect_network_health(arguments.target)
    services = collect_service_health()
    event_log = check_recent_event_errors(arguments.event_hours)

    health["network"] = network
    health["services"] = services
    health["event_log"] = event_log

    json_report_path = save_json_report(health)
    html_report_path = save_html_report(health)

    print("\nSYSTEM HEALTH REPORT")
    print("=" * 60)
    print(f"Time     : {health['timestamp']}")
    print(f"Computer : {health['hostname']}")
    print(f"OS       : {health['operating_system']}")
    print("-" * 60)

    display_metric("CPU", health["cpu"])
    display_metric("Memory", health["memory"])
    display_metric("Disk", health["disk"])

    print("\nNETWORK CHECKS")
    print("-" * 60)

    dns = network["dns"]
    print(
        f"DNS      : {dns['target']} -> "
        f"{dns['ip_address']} [{dns['status']}]"
    )

    https = network["https"]
    print(
        f"TCP/443  : {https['target']}:{https['port']} "
        f"[{https['status']}]"
    )

    print("\nWINDOWS SERVICE CHECKS")
    print("-" * 60)

    for service in services:
        print(
            f"{service['display_name']:<20}: "
            f"{service['current_status']:<13} "
            f"[{service['status']}]"
        )

    print("\nWINDOWS EVENT LOG")
    print("-" * 60)

    error_count = event_log["error_count"]
    count_display = "unknown" if error_count is None else error_count

    print(
        f"{event_log['log_name']} log, last "
        f"{event_log['lookback_hours']} hours: "
        f"{count_display} critical/error events "
        f"[{event_log['status']}]"
    )

    print("=" * 60)
    print(f"JSON report saved: {json_report_path.resolve()}")
    print(f"HTML report saved: {html_report_path.resolve()}")


if __name__ == "__main__":
    main()