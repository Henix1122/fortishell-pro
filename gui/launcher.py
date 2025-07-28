def launch_gui():
    import subprocess
    import sys
    # Launch the GTK GUI as a separate process
    subprocess.Popen([sys.executable, 'gui/gtk_gui.py'])

if __name__ == "__main__":
    launch_gui()
