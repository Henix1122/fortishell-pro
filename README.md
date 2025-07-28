# 🔐 FortiShell Pro (Advanced Edition)

FortiShell Pro is an advanced, cross-platform cybersecurity suite designed for professionals, ethical hackers, and power users. Its modular architecture integrates CLI and GUI interfaces for maximum flexibility and productivity. Effortlessly perform deep diagnostics, advanced password analysis, phishing detection, SSL/TLS validation, and real-time file integrity monitoring—all in one unified toolkit. Built for extensibility, automation, and robust reporting, FortiShell Pro empowers you to secure, audit, and monitor any environment with confidence.

---

## Advanced Features

- Modular CLI and GUI
- File Integrity Checker
- Password Analyzer
- SSL Validator
- Real-time monitoring
- Advanced error handling and logging
- Requires root permission for full functionality

### CLI

All module commands must be run via `main.py` with root privileges. For development, you may run module scripts directly as shown below.

```bash
# General usage (run as root):
sudo python main.py <command> [arguments]

# Examples:
sudo python main.py password "G@naStrong2025"
sudo python main.py ssl example.com
sudo python main.py url http://example.com
sudo python main.py integrity README.md
```

#### Commands

- `about` - Show about info
- `man` - Show manual
- `export` - Export latest report
- `config` - Open config file
- `gui` - Launch GUI dashboard
- `integrity <file>` - File integrity check
- `password <password>` - Password analyzer
- `ssl <domain>` - SSL validator
- `url <url>` - URL checker
- `monitor` - File monitor
- `sysinfo` - System info
- `pyenv` - Python env info
- `cli` - CLI launcher (GUI)
- `feedback` - Feedback/issues (GUI)

#### Options

- `--gui` - Launch GUI dashboard
- `--export` - Export latest report
- `--config` - Open config file
- `--log` - Open log file
- `--report` - Open report file
- `--dark` - Enable dark mode in GUI
- `--sysinfo` - Show system information (CLI/GUI)
- `--pyenv` - Show Python environment information (CLI/GUI)
- `--cli` - Open CLI launcher in GUI
- `--feedback` - Open feedback/issues panel in GUI

### GUI

Launch with root privileges:

```bash
# Launch GUI (recommended, as root)
sudo python main.py gui
# or
sudo python main.py --gui
# Or run the packaged executable (after building):
sudo ./dist/FortiShellPro
```

Features:
- All modules accessible via dashboard
- About, Manual, Export, Config, Open Log, Open Config, Open Reports
- Dark Mode toggle
- System Info panel (CLI/GUI)
- Python Env Info panel (CLI/GUI)
- CLI Launcher (GUI)
- Feedback/Issues button (GUI)
- Fully cross-platform packaging (Windows, Linux, macOS)

## Advanced Error Handling

All commands and modules feature robust error handling and logging. See `reports/report.txt` and logs for details.

---

## 📦 Packaging & Distribution (All OS)

FortiShell Pro can be packaged as a standalone executable for Windows, Linux, and macOS using PyInstaller. The packaged app should be run with root privileges for full functionality.

### Build Instructions

1. Install PyInstaller:
    ```bash
    pip install pyinstaller
    # or (Linux)
    sudo apt install pyinstaller
    ```
2. Build the executable:
    ```bash
    pyinstaller fortishell-pro.spec
    # Output will be in dist/FortiShellPro
    ```
    - For Windows, use a `.ico` icon; for macOS, use `.icns`; for Linux, `.png` is fine (icon is ignored on Linux).
    - All assets, icons, and modules are included automatically.
3. Run the app:
    ```bash
    ./dist/FortiShellPro
    ```
4. For CLI only:
    ```bash
    python main.py <command> [arguments]
    ```

---
│   ├── url_panel.py
│   ├── password_panel.py
│   ├── integrity_panel.py
│   └── launcher.py
│
└── assets/
     └── icons/
```

---

## 🧠 Advanced Command Buffet

```bash
# Launch CLI (main entry)
python main.py --help

# Launch GUI (recommended)
python main.py gui
# Or run the packaged executable (after building):
./dist/FortiShellPro

# SSL Certificate Validator (modular)
python main.py ssl example.com
python modules/ssl_validator.py --host example.com --port 443

# Phishing Detector (modular)
python main.py url http://suspicious.site
python modules/url_checker.py --url http://suspicious.site

# Password Analyzer (modular)
python main.py password "G@naStrong2025!"
python modules/password_analyzer.py --password "G@naStrong2025!"

# File Integrity Monitor (modular)
python main.py integrity /path/to/file --algorithm sha256
python modules/file_integrity.py --file /path/to/file --algorithm sha256

# Config & Logs (advanced)
python config_tool.py --set gui.theme=dark
python config_tool.py --get gui.theme

# Export/Report (utility)
python -c "from utils.report_export import export_report; export_report({'result':'ok'}, 'myreport.txt')"

# Debug & Dev Utilities
python dev_tools/debug_panel.py --module phishing_detector

# Help/About/Manual
python main.py --help
python main.py ssl --help
python main.py url --help
python main.py password --help
python main.py integrity --help
```

---

## 🔐 Advanced SSL Certificate Validator

```bash
python ssl_validator.py --host example.com --port 443
```
- Checks expiry, issuer, CN mismatch, and trust chain
- Extend with `--verbose`, `--output log.txt`

---

## 🕵️ Advanced Phishing Detector

```bash
python phishing_detector.py --url http://suspicious.site
```
- Parses domain features, DNS inconsistencies, known blacklists
- Add `--deep-scan` for full page analysis

---

## 🔑 Advanced Password Analyzer

```bash
python password_analyzer.py --password "G@naStrong2025!"
```
- Returns entropy, breach status (via API), and recommendations
- Optional `--local-db` for offline analysis

---

## 🔍 Advanced File Integrity Monitor

```bash
python integrity_monitor.py --path /folder/to/watch
```
- Baselines hashes, monitors changes, flags deletions/insertions
- Add `--log changes.json` to store tracking data

---

## ⚙️ Advanced Config & Logs

```bash
python config_tool.py --set gui.theme=dark
python config_tool.py --get gui.theme
```

---

## 🧪 Advanced Debug & Dev Utilities

```bash
python dev_tools/debug_panel.py --module phishing_detector
```
- Opens internal logs and error traces for selected module

---

## ⚡ Real-time Help Menu

Ask for `help_menu.py` to get interactive descriptions and usage links for every command.

---

## 🆘 Help / Manual

Run `python main.py -h` for full command list and options.

Each subcommand supports `-h` for details, e.g.:
```
python main.py ssl -h
python main.py url -h
python main.py password -h
python main.py integrity -h
```

---

## ℹ️ About

- Author: FortiShell Pro Team
- License: MIT
- Python 3.7+
- Dependencies: See requirements.txt
- Contributions welcome!
GitHub: https://github.com/Henix1122/fortishell-pro

---

## 📖 Advanced Manual (man)

### Usage

#### CLI (run as root)
```bash
sudo python main.py <command> [arguments]
# Example:
sudo python main.py password "G@naStrong2025!"
sudo python main.py ssl example.com
sudo python main.py url http://example.com
sudo python main.py integrity README.md
```

#### GUI (run as root)
```bash
sudo python main.py gui
# Or run the packaged executable:
sudo ./dist/FortiShellPro
```

All modules and features are accessible via both CLI and GUI. See above for advanced commands and packaging instructions.

---

## 🛠️ Advanced Setup

1. Clone the repo
2. `pip install -r requirements.txt`
3. Run with `python main.py` or launch the GUI

---

## Advanced Usage

- All output is logged to `fortishell.log`.
- Reports are saved in `/reports/report.txt`.
- Easily extend by adding modules to `/modules` and GUI panels to `/gui`.
- Always run with root privileges for full access to system features.

---

## Disclaimer

For educational and authorized security testing only. Use responsibly.

📜 License

Open-source under MIT License. Free to use, modify, and share.

🙌 Credits

Made by [Michael], cybersecurity builder and toolmaker. Inspired by real-world needs, built for clarity, speed, and accessibility.
