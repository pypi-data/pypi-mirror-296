# NoLimit Scanner

NoLimit: An advanced, asynchronous port scanner and service enumerator built in Python. Inspired by Masscan, it offers high-speed scanning capabilities with customizable options for both TCP and UDP protocols. NoLimit provides a quick approach to port enumeration, designed for efficiency and speed.

## Features

- **Asynchronous Scanning**: Utilizes Python's asyncio for high-performance, concurrent scanning.
- **TCP and UDP Support**: Scan both TCP and UDP ports with a single tool.
- **Service Detection**: Integrates with Nmap for accurate service and version detection.
- **Scapy Integration**: Optional use of Scapy for customized packet crafting to evade firewalls.
- **Adaptive Scanning**: Automatically adjusts worker count based on open ports found for optimal performance.
- **Resume Functionality**: Ability to resume interrupted scans from the last saved progress.
- **Rate Limiting**: Control scan intensity to avoid overwhelming target networks.
- **Customizable Workers**: Adjust the number of concurrent workers to balance speed and resource usage.
- **Progress Tracking**: Real-time progress bar and ETA using tqdm.
- **Colorized Output**: Easy-to-read, color-coded console output for better visibility.

## Installation

### Option 1: Install from PyPI

To install NoLimit directly from PyPI, run:
```pip install nolimit```

### Option 2: Build from Source

1. Clone the repository:
   ```
   git clone https://github.com/jivy26/nolimit-scanner.git
   cd nolimit-scanner
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Example usage:
`python nolimit.py -p 1-4000 -i ips.txt -t -w 1000 -srv`
This example scans TCP ports 1-4000 for IPs listed in ips.txt, using 1000 workers and enabling Nmap service detection.

### Options

- `-p, --ports`: Ports to scan (e.g., "80,443" or "1-1024"). Default: all ports.
- `-i, --ip`: [Required] Single IP or file with list of IPs to scan.
- `-t, --tcp`: Enable TCP port scanning.
- `-u, --udp`: Enable UDP port scanning.
- `-srv, --service`: Enable service detection with Nmap.
- `-w, --workers`: Number of concurrent workers (default: 500).
- `--scapy`: Use Scapy for scanning (helps evade firewalls). **Recommend running against only tcpwrapped ports identified, as running on all ports will take a while**
- `--resume`: Resume from the last saved progress.
- `--adaptive`: Use adaptive scanning to adjust worker count dynamically.
- `--rate-limit`: Set rate limit in packets per second.

## Output

NoLimit generates several output files:

1. Real-time console output with color-coded results.
2. Protocol-specific folders (e.g., `tcp_1234`, `udp_5678`) containing:
   - `summary.txt`: Comprehensive summary of all scanned ports and services.
   - Specific host files for common ports (e.g., `http-hosts.txt`, `ssh-hosts.txt`).
   - `web-urls.txt`: List of discovered web URLs.
   - `[protocol]_other_ports.txt`: List of open ports not covered by specific files.

When service detection is enabled, a detailed table of services and versions is displayed in the console.

## Warnings and Ethical Use

**IMPORTANT**: Improper use on networks without explicit permission may be illegal and unethical. Always ensure you have proper authorization before scanning any network or system you do not own.
