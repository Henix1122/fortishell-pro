import os
import sys

# Enforce root permission
if os.name != 'nt' and os.geteuid() != 0:
    print("[ERROR] FortiShell Pro must be run as root. Use 'sudo python main.py ...' or 'sudo ./dist/FortiShellPro'.")
    sys.exit(1)
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Core utility modules
from utils.logger import setup_logger
from utils.report_export import export_report

# Security modules
from modules.ssl_validator import check_ssl_cert
from modules.url_checker import check_phishing_url
from modules.password_analyzer import analyze_password
from modules.file_integrity import verify_file_hash

console = Console()
logger = setup_logger()


def show_banner():
    banner = Text()
    banner.append("\n🛡️ FORTISHELL PRO\n", style="bold cyan")
    banner.append("Built for multi-OS defense. Powered by Python.\n", style="italic green")
    banner.append("Type 'python main.py man' or 'python main.py about' for more info.\n", style="bold yellow")
    console.print(banner)

def show_about():
    about = Panel("""
FortiShell Pro v1.0
Modular cybersecurity toolkit (CLI + GUI)
Author: FortiShell Pro Team
License: MIT
Python 3.7+
""", title="About", style="bold blue")
    console.print(about)

def show_manual():
    man = Panel("""
Commands:
  ssl <domain>         Validate SSL certificate
  url <url>            Check URL for phishing
  password <pw>        Analyze password strength
  integrity <file>     Check file integrity
  gui                  Launch GUI
  export <file>        Export last report to file
  config <key> <val>   Set config (future)
  sysinfo              Show system information (CLI/GUI)
  pyenv                Show Python environment info (CLI/GUI)
  cli                  Open CLI launcher (GUI)
  feedback             Feedback/issues (GUI)
  about                Show about info
  man                  Show this manual
Use -h on any command for details.
""", title="Manual", style="bold magenta")
    console.print(man)

def run_export(args):
    try:
        with open('reports/report.txt') as f:
            data = f.read()
        export_report(data, args.file)
        console.print(f"[green]Exported report to {args.file}[/green]")
    except Exception as e:
        console.print(f"[red]Export failed: {e}[/red]")

def run_config(args):
    # Placeholder for config set/get
    console.print(f"[yellow]Config command not yet implemented. Key: {args.key}, Value: {args.value}[/yellow]")

def run_gui(args=None):
    try:
        import subprocess
        subprocess.run(["python", "-m", "gui.launcher"])
    except Exception as e:
        console.print(f"[red]Failed to launch GUI: {e}[/red]")

def run_ssl(args):
    logger.info(f"SSL check requested for {args.domain}")
    console.print(Panel(f"🔐 SSL Certificate Check for [bold cyan]{args.domain}[/bold cyan]", style="bold green"))
    cert = check_ssl_cert(args.domain)
    if isinstance(cert, str):
        console.print(f"[red]{cert}[/red]")
        export_report(cert)
    else:
        table = Table(title="SSL Details", style="cyan")
        table.add_column("Field", style="bold")
        table.add_column("Value")
        for k, v in cert.items():
            table.add_row(k, str(v))
        console.print(table)
        export_report(str(cert))

def run_url(args):
    logger.info(f"Phishing check for URL: {args.url}")
    verdict = check_phishing_url(args.url)
    color = "green" if verdict == "Safe" else "red"
    console.print(Panel(f"🕸️ Phishing Detector for [bold cyan]{args.url}[/bold cyan]", style="bold green"))
    console.print(f"[bold {color}]Verdict: {verdict}[/bold {color}]")
    export_report(f"URL: {args.url}\nVerdict: {verdict}")

def run_password(args):
    logger.info("Password analysis triggered")
    console.print(Panel("🔐 Password Strength Analyzer", style="bold green"))
    result = analyze_password(args.password)
    content = ""
    for key, value in result.items():
        console.print(f"[bold cyan]{key}:[/bold cyan] {value}")
        content += f"{key}: {value}\n"
    export_report(content)

def run_integrity(args):
    logger.info(f"File integrity check on {args.file} using {args.algorithm}")
    console.print(Panel("📦 File Integrity Monitor", style="bold green"))
    try:
        hash_result = verify_file_hash(args.file)
        if isinstance(hash_result, str) and hash_result.startswith("File hash error"):
            console.print(f"[red]{hash_result}[/red]")
            export_report(hash_result)
        else:
            console.print(f"[bold cyan]Hash:[/bold cyan] {hash_result}")
            export_report(f"File: {args.file}\nHash: {hash_result}")
    except Exception as e:
        console.print(f"[red]Integrity check failed: {e}[/red]")
        export_report(f"Integrity check failed: {e}")


def main():
    show_banner()
    parser = argparse.ArgumentParser(description="FortiShell Pro - Modular Security Toolkit")
    subparsers = parser.add_subparsers(dest='command')

    ssl_parser = subparsers.add_parser("ssl", help="Validate SSL certificate")
    ssl_parser.add_argument("domain", help="Target domain")
    ssl_parser.set_defaults(func=run_ssl)

    url_parser = subparsers.add_parser("url", help="Check URL for phishing")
    url_parser.add_argument("url", help="Target URL")
    url_parser.set_defaults(func=run_url)

    pwd_parser = subparsers.add_parser("password", help="Analyze password strength")
    pwd_parser.add_argument("password", help="Password to analyze")
    pwd_parser.set_defaults(func=run_password)

    file_parser = subparsers.add_parser("integrity", help="Check file integrity")
    file_parser.add_argument("file", help="File path")
    file_parser.add_argument("--algorithm", default="sha256", help="Hashing algorithm (default: sha256)")
    file_parser.set_defaults(func=run_integrity)

    export_parser = subparsers.add_parser("export", help="Export last report to file")
    export_parser.add_argument("file", help="Output file path")
    export_parser.set_defaults(func=run_export)

    config_parser = subparsers.add_parser("config", help="Set or get configuration")
    config_parser.add_argument("key", help="Config key")
    config_parser.add_argument("value", nargs="?", help="Config value (optional)")
    config_parser.set_defaults(func=run_config)

    gui_parser = subparsers.add_parser("gui", help="Launch the GUI application")
    gui_parser.set_defaults(func=run_gui)

    about_parser = subparsers.add_parser("about", help="Show about info")
    about_parser.set_defaults(func=lambda args: show_about())

    man_parser = subparsers.add_parser("man", help="Show manual/help")
    man_parser.set_defaults(func=lambda args: show_manual())

    # Add advanced feature commands
    sysinfo_parser = subparsers.add_parser("sysinfo", help="Show system information (CLI/GUI)")
    sysinfo_parser.set_defaults(func=run_sysinfo)

    pyenv_parser = subparsers.add_parser("pyenv", help="Show Python environment info (CLI/GUI)")
    pyenv_parser.set_defaults(func=run_pyenv)

    cli_parser = subparsers.add_parser("cli", help="Open CLI launcher (GUI)")
    cli_parser.set_defaults(func=run_cli_launcher)

    feedback_parser = subparsers.add_parser("feedback", help="Feedback/issues (GUI)")
    feedback_parser.set_defaults(func=run_feedback)

    try:
        args = parser.parse_args()
        if hasattr(args, 'func'):
            args.func(args)
        else:
            parser.print_help()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        console.print(f"[red]Fatal error: {e}[/red]")

# --- Advanced feature handlers ---
def run_sysinfo(args):
    import psutil
    import platform
    console.print("\n[bold magenta]System Information:[/bold magenta]")
    console.print(f"Platform: {platform.system()} {platform.release()}")
    console.print(f"Processor: {platform.processor()}")
    console.print(f"CPU Cores: {psutil.cpu_count(logical=False)} physical / {psutil.cpu_count()} logical")
    console.print(f"Memory: {round(psutil.virtual_memory().total / (1024**3), 2)} GB")

def run_pyenv(args):
    import sys
    import pkg_resources
    console.print("\n[bold magenta]Python Environment Info:[/bold magenta]")
    console.print(f"Python: {sys.version}")
    console.print("Installed packages:")
    for dist in pkg_resources.working_set:
        console.print(f"- {dist.project_name} {dist.version}")

def run_cli_launcher(args):
    try:
        import subprocess
        subprocess.run(["python", "-m", "gui.launcher", "--tab", "cli"])
    except Exception as e:
        console.print(f"[red]Failed to launch CLI tab in GUI: {e}[/red]")

def run_feedback(args):
    try:
        import subprocess
        subprocess.run(["python", "-m", "gui.launcher", "--tab", "feedback"])
    except Exception as e:
        console.print(f"[red]Failed to launch Feedback tab in GUI: {e}[/red]")

if __name__ == "__main__":
    main()
