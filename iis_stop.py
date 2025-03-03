import subprocess
import ctypes
import sys
from app_main import client_name, site_name
from app_log_utils import write_log

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def stop_iis_site(site_name):
    try:
        subprocess.run(["powershell", "-Command", f"Stop-Website -Name '{site_name}'"], check=True)
        print(f"Site '{site_name}' stopped successfully.")
        return True, []  # Success, no errors
    except subprocess.CalledProcessError as e:
        print(f"Failed to stop the site: {e.stderr}")
        return False, [str(e)]  # Failure, with error details

if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        success, errors = stop_iis_site(site_name)
        # Log the result (assuming log_file and s_no are passed or managed globally)
        # Example: write_log(log_file, s_no, "iis_stop.py", client_name, success, not success, errors)