# Yaphit - Yet Another Phishing Tool

## Overview

**Yaphit** (Yet Another Phishing Tool) is a tool designed for **PenTesting** and **Red Team** operations. It allows users to quickly clone login pages and host them on a local webserver. This tool can be used to simulate phishing attacks by duplicating legitimate login pages, enabling security professionals to test and assess the phishing vulnerability of their target systems.

Yaphit is intended for **ethical hacking** purposes only. By replicating login forms and capturing user input, security experts can analyze and test how users might be lured into submitting sensitive information such as credentials.

## Features

- **Fast cloning of login pages**: Automatically downloads and sets up a copy of a website's login page.
- **Launches a simple HTTP server**: Hosts the cloned page on your machine for easy access.
- **Customizable user-agent**: Simulate different browsers or environments while making web requests.
- **Form data capture**: All form submissions are logged and saved for analysis.
- **Built-in clearing mechanism**: Clear the server directory and prepare for new cloning operations.
- **Redirection**: Allows forwarding of requests to a specific IP or domain after the form is submitted.

## Installation

### Prerequisites

- Python 3.x
- [Wget](https://www.gnu.org/software/wget/) installed and available in your system's PATH.

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/yaphit.git
   cd yaphit
   ```
2. Install necessary Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

To clone a login page and host it on your server, simply provide the URL and specify the port for the HTTP server:

```bash
python3 yaphit.py --url "http://example.com/login" --port 8080
```

### Options

- `--url`: The URL of the login page to clone (required unless `--clear` is used).
- `--port`: The port to serve the HTTP server (default: 80).
- `--user_agent`: Custom user agent for the wget request (default: Fedora/Firefox).
- `--redirect_ip`: IP/domain to redirect GET/POST requests after form submission (default: the URL provided).
- `--clear`: Clears the `/site` directory before running the tool again.

### Clear the Site Directory

Before cloning a new page, you might want to clear the existing content from the `/site` folder:

```bash
python3 yaphit.py --clear
```

### Example

Here's a typical use case of cloning a login page and hosting it on port 8080:

```bash
python3 yaphit.py --url "http://example.com/login" --port 8080
```

After cloning, the tool will modify the form action, start a local server, and capture any form submissions. All captured data will be logged in the `posts/` directory.

### Greets

this tool is the result of some modifications of the original tool httphish (https://github.com/miguelangelramirez/httphish)

## Disclaimer

**Yaphit** is strictly for **ethical purposes** in penetration testing, red teaming, and security assessments. It is illegal to use this tool for unauthorized phishing or attacks. Use only with explicit permission from the target or as part of sanctioned security assessments.

The developer does not assume any responsibility for misuse or damage caused by this tool.
