import json
from datetime import datetime
from html import escape
from pathlib import Path


def save_json_report(data, report_directory="reports"):
    """Save collected data as a timestamped JSON report."""
    output_directory = Path(report_directory)
    output_directory.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_path = output_directory / f"system-health-{timestamp}.json"

    with report_path.open("w", encoding="utf-8") as report_file:
        json.dump(data, report_file, indent=4)

    return report_path


def save_html_report(data, report_directory="reports"):
    """Save collected data as a readable HTML report."""
    output_directory = Path(report_directory)
    output_directory.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_path = output_directory / f"system-health-{timestamp}.html"

    service_rows = "".join(
        f"""
        <tr>
            <td>{escape(service["display_name"])}</td>
            <td>{escape(service["current_status"])}</td>
            <td class="{service["status"].lower()}">
                {escape(service["status"])}
            </td>
        </tr>
        """
        for service in data["services"]
    )

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>System Health Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            background: #f4f7fb;
            color: #1f2937;
        }}
        h1, h2 {{ color: #17365d; }}
        .card {{
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px #cccccc;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 10px;
            border-bottom: 1px solid #dddddd;
            text-align: left;
        }}
        .ok {{ color: green; font-weight: bold; }}
        .warning {{ color: #d97706; font-weight: bold; }}
        .failed {{ color: red; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>IT Operations System Health Report</h1>

    <div class="card">
        <p><strong>Generated:</strong> {escape(data["timestamp"])}</p>
        <p><strong>Computer:</strong> {escape(data["hostname"])}</p>
        <p><strong>Operating system:</strong>
            {escape(data["operating_system"])}</p>
    </div>

    <div class="card">
        <h2>System Resources</h2>
        <table>
            <tr><th>Resource</th><th>Usage</th><th>Status</th></tr>
            <tr>
                <td>CPU</td>
                <td>{data["cpu"]["usage_percent"]}%</td>
                <td class="{data["cpu"]["status"].lower()}">
                    {data["cpu"]["status"]}
                </td>
            </tr>
            <tr>
                <td>Memory</td>
                <td>{data["memory"]["usage_percent"]}%</td>
                <td class="{data["memory"]["status"].lower()}">
                    {data["memory"]["status"]}
                </td>
            </tr>
            <tr>
                <td>Disk</td>
                <td>{data["disk"]["usage_percent"]}%</td>
                <td class="{data["disk"]["status"].lower()}">
                    {data["disk"]["status"]}
                </td>
            </tr>
        </table>
    </div>

    <div class="card">
        <h2>Network Checks</h2>
        <p><strong>DNS:</strong>
            {escape(data["network"]["dns"]["target"])} →
            {escape(str(data["network"]["dns"]["ip_address"]))}
            [{escape(data["network"]["dns"]["status"])}]
        </p>
        <p><strong>TCP/443 reachability:</strong>
            {escape(data["network"]["https"]["target"])}:443
            [{escape(data["network"]["https"]["status"])}]
        </p>
    </div>

    <div class="card">
        <h2>Windows Services</h2>
        <table>
            <tr><th>Service</th><th>State</th><th>Status</th></tr>
            {service_rows}
        </table>
    </div>

    <div class="card">
        <h2>Windows Event Log</h2>
        <p>
            Errors in the last {data["event_log"]["lookback_hours"]} hours:
            <strong>{data["event_log"]["error_count"]}</strong>
            [{escape(data["event_log"]["status"])}]
        </p>
    </div>
</body>
</html>
"""

    report_path.write_text(html_content, encoding="utf-8")
    return report_path