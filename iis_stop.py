import subprocess
import ctypes
import sys
from app_main import client_name, site_name, log_file
from log import write_log

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def stop_iis_site(site_name):
    try:
        subprocess.run(["powershell", "-Command", f"Stop-Website -Name '{site_name}'"], check=True)
        print(f"Site '{site_name}' stopped successfully.")
        write_log(log_file, 1, "iis_stop.py", client_name, 1, 0, [])  # Log success
    except subprocess.CalledProcessError as e:
        print(f"Failed to stop the site: {e.stderr}")
        write_log(log_file, 1, "iis_stop.py", client_name, 0, 1, [e.stderr])  # Log failure

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
else:
    stop_iis_site(site_name)