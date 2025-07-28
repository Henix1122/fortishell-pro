import os
import sys

# Enforce root permission
if os.name != 'nt' and os.geteuid() != 0:
    print("[ERROR] FortiShell Pro GUI must be run as root. Use 'sudo python main.py gui' or 'sudo ./dist/FortiShellPro'.")
    sys.exit(1)

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

# Import all required modules at the top for clarity and performance
try:
    from ssl_panel import SSLPanelPro
except ImportError:
    SSLPanelPro = None

try:
    from modules.ssl_validator import check_ssl_cert
    from modules.url_checker import check_phishing_url, check_malware_url, check_blacklist_url
    from modules.password_analyzer import analyze_password, password_strength_score
    from modules.file_integrity import verify_file_hash
except ImportError:
    check_ssl_cert = check_phishing_url = check_malware_url = check_blacklist_url = None
    analyze_password = password_strength_score = None
    verify_file_hash = None

def set_textview_text(textview, text):
    buf = textview.get_buffer()
    buf.set_text(str(text))

def show_error_dialog(parent, message):
    dialog = Gtk.MessageDialog(
        transient_for=parent,
        flags=0,
        message_type=Gtk.MessageType.ERROR,
        buttons=Gtk.ButtonsType.CLOSE,
        text="Error",
    )
    dialog.format_secondary_text(message)
    dialog.run()
    dialog.destroy()

class FortiShellGTK(Gtk.Window):
    def __init__(self):
        super().__init__(title="FortiShell Pro")
        self.set_border_width(10)
        self.set_default_size(900, 650)
        self.set_icon_name("security-high")
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(True)

        notebook = Gtk.Notebook()
        notebook.set_scrollable(True)
        self.add(notebook)

        # SSL Validator Tab
        ssl_tab = SSLPanelPro() if SSLPanelPro else Gtk.Label(label="Advanced SSL Panel not found.")
        notebook.append_page(ssl_tab, Gtk.Label(label="SSL Validator Pro"))

        # URL Checker Tab
        url_tab = self.create_url_checker_tab()
        notebook.append_page(url_tab, Gtk.Label(label="URL Checker"))

        # Password Analyzer Tab
        pw_tab = self.create_password_analyzer_tab()
        notebook.append_page(pw_tab, Gtk.Label(label="Password Analyzer"))

        # File Integrity Tab
        file_tab = self.create_file_integrity_tab()
        notebook.append_page(file_tab, Gtk.Label(label="File Integrity Pro"))

    def create_url_checker_tab(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        grid = Gtk.Grid(column_spacing=8, row_spacing=8)
        box.pack_start(grid, False, False, 0)

        entry = Gtk.Entry()
        entry.set_placeholder_text("Enter URL (e.g., https://example.com)")
        grid.attach(Gtk.Label(label="URL:"), 0, 0, 1, 1)
        grid.attach(entry, 1, 0, 2, 1)

        mode_combo = Gtk.ComboBoxText()
        for mode in ["Phishing Check", "Malware Check", "Blacklist Check"]:
            mode_combo.append_text(mode)
        mode_combo.set_active(0)
        grid.attach(Gtk.Label(label="Mode:"), 0, 1, 1, 1)
        grid.attach(mode_combo, 1, 1, 2, 1)

        button = Gtk.Button(label="Check URL")
        grid.attach(button, 1, 2, 1, 1)

        progress = Gtk.ProgressBar()
        progress.set_show_text(True)
        progress.set_text("Ready")
        grid.attach(progress, 2, 2, 1, 1)

        output = Gtk.TextView()
        output.set_editable(False)
        output.set_wrap_mode(Gtk.WrapMode.WORD)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_min_content_height(120)
        scrolled.add(output)
        box.pack_start(scrolled, True, True, 0)

        def on_check(_):
            url = entry.get_text().strip()
            mode = mode_combo.get_active_text()
            progress.set_fraction(0.3)
            progress.set_text("Checking...")
            while Gtk.events_pending():
                Gtk.main_iteration()
            try:
                if not url:
                    raise ValueError("URL cannot be empty.")
                if mode == "Phishing Check" and check_phishing_url:
                    result = check_phishing_url(url)
                elif mode == "Malware Check" and check_malware_url:
                    result = check_malware_url(url)
                elif mode == "Blacklist Check" and check_blacklist_url:
                    result = check_blacklist_url(url)
                else:
                    result = "Unknown mode or module not available."
            except Exception as e:
                result = f"Error: {e}"
                show_error_dialog(self, result)
            set_textview_text(output, result)
            progress.set_fraction(1.0)
            progress.set_text("Done")

        button.connect("clicked", on_check)
        return box

    def create_password_analyzer_tab(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        grid = Gtk.Grid(column_spacing=8, row_spacing=8)
        box.pack_start(grid, False, False, 0)

        entry = Gtk.Entry()
        entry.set_placeholder_text("Enter password")
        grid.attach(Gtk.Label(label="Password:"), 0, 0, 1, 1)
        grid.attach(entry, 1, 0, 2, 1)

        visibility = Gtk.CheckButton(label="Show Password")
        grid.attach(visibility, 1, 1, 1, 1)

        strength_bar = Gtk.ProgressBar()
        strength_bar.set_show_text(True)
        strength_bar.set_text("Strength: N/A")
        grid.attach(strength_bar, 2, 1, 1, 1)

        button = Gtk.Button(label="Analyze Password")
        grid.attach(button, 1, 2, 1, 1)

        output = Gtk.TextView()
        output.set_editable(False)
        output.set_wrap_mode(Gtk.WrapMode.WORD)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_min_content_height(120)
        scrolled.add(output)
        box.pack_start(scrolled, True, True, 0)

        def on_visibility_toggled(btn):
            entry.set_visibility(btn.get_active())
        visibility.connect("toggled", on_visibility_toggled)

        def on_entry_changed(_):
            pw = entry.get_text()
            try:
                if password_strength_score:
                    score, verdict = password_strength_score(pw)
                    strength_bar.set_fraction(score / 100.0)
                    strength_bar.set_text(f"Strength: {verdict}")
                else:
                    strength_bar.set_fraction(0)
                    strength_bar.set_text("Strength: N/A")
            except Exception:
                strength_bar.set_fraction(0)
                strength_bar.set_text("Strength: N/A")
        entry.connect("changed", on_entry_changed)

        def on_analyze(_):
            pw = entry.get_text()
            try:
                if not pw:
                    raise ValueError("Password cannot be empty.")
                result = analyze_password(pw) if analyze_password else "Module not available."
            except Exception as e:
                result = f"Error: {e}"
                show_error_dialog(self, result)
            set_textview_text(output, result)

        button.connect("clicked", on_analyze)
        return box

    def create_file_integrity_tab(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        grid = Gtk.Grid(column_spacing=8, row_spacing=8)
        box.pack_start(grid, False, False, 0)

        entry = Gtk.Entry()
        entry.set_placeholder_text("Enter file path (e.g., /home/user/file.txt)")
        grid.attach(Gtk.Label(label="File Path:"), 0, 0, 1, 1)
        grid.attach(entry, 1, 0, 2, 1)

        chooser = Gtk.FileChooserButton(title="Select a file", action=Gtk.FileChooserAction.OPEN)
        grid.attach(chooser, 1, 1, 2, 1)

        button = Gtk.Button(label="Check Integrity")
        grid.attach(button, 1, 2, 1, 1)

        progress = Gtk.ProgressBar()
        progress.set_show_text(True)
        progress.set_text("Ready")
        grid.attach(progress, 2, 2, 1, 1)

        output = Gtk.TextView()
        output.set_editable(False)
        output.set_wrap_mode(Gtk.WrapMode.WORD)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_min_content_height(120)
        scrolled.add(output)
        box.pack_start(scrolled, True, True, 0)

        def on_file_selected(widget):
            selected_file = widget.get_filename()
            if selected_file:
                entry.set_text(selected_file)
        chooser.connect("file-set", on_file_selected)

        def on_check(_):
            file_path = entry.get_text().strip()
            progress.set_fraction(0.3)
            progress.set_text("Checking...")
            while Gtk.events_pending():
                Gtk.main_iteration()
            try:
                if not file_path:
                    raise ValueError("File path cannot be empty.")
                result = verify_file_hash(file_path) if verify_file_hash else "Module not available."
            except Exception as e:
                result = f"Error: {e}"
                show_error_dialog(self, result)
            set_textview_text(output, result)
            progress.set_fraction(1.0)
            progress.set_text("Done")

        button.connect("clicked", on_check)
        return box

win = FortiShellGTK()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
