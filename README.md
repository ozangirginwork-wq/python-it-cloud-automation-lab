# Python IT Operations Automation Toolkit

A Windows-focused Python automation toolkit that performs system health checks, validates network connectivity, monitors essential Windows services, reviews recent event-log errors, and generates JSON and HTML reports.

## Features

- CPU, memory, and disk utilization monitoring
- Configurable 80% warning threshold
- DNS resolution testing
- HTTPS port 443 connectivity testing
- Windows service monitoring
- Windows Application event-log error detection
- Timestamped JSON reports
- Styled HTML reports
- Configurable command-line options
- Automated tests with pytest

## Project Structure

```text
python-it-cloud-automation-lab/
├── main.py
├── requirements.txt
├── src/
│   ├── event_log_checks.py
│   ├── network_checks.py
│   ├── reporting.py
│   ├── service_checks.py
│   └── system_health.py
├── tests/
│   └── test_system_health.py
└── reports/
    ├── sample-report.html
    └── sample-report.json
```

## Installation

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
python -m pip install -r requirements.txt
```

## Usage

Run with the default settings:

```powershell
python main.py
```

Run with a custom network target and event-log period:

```powershell
python main.py --target microsoft.com --event-hours 12
```

Available options:

- `--target` selects the hostname used for DNS and HTTPS tests.
- `--event-hours` selects how many hours of Windows Application events to inspect.

## Generated Reports

Each execution creates:

- A JSON report for automation and further processing
- A styled HTML report for human review

Portfolio samples:

- [Sample HTML report](reports/sample-report.html)
- [Sample JSON report](reports/sample-report.json)

## Automated Tests

Run the test suite:

```powershell
python -m pytest -v
```

Current result:

```text
3 passed
```

## Technologies

- Python
- psutil
- pytest
- PowerShell
- Windows Event Log
- Git

## Security and Safety

The toolkit performs read-only diagnostic checks. It does not modify services, event logs, network settings, or system configuration.

## Skills Demonstrated

- Python scripting and modular project design
- Windows systems administration
- Resource and service monitoring
- DNS and TCP connectivity troubleshooting
- Event-log analysis
- JSON and HTML report generation
- Command-line interface development
- Automated testing
- Git version control