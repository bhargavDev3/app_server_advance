import subprocess
import ctypes
import sys
from app_main import client_name, site_name

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def start_iis_site(site_name):
    try:
        subprocess.run(["powershell", "-Command", f"Start-Website -Name '{site_name}'"], check=True)
        print(f"Site '{site_name}' started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start the site: {e.stderr}")

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
else:
    start_iis_site(site_name)