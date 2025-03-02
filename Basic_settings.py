import subprocess
import ctypes
import sys
from app_main import client_name, date, app_pool_name, site_name, application_name
from log_utils import write_log

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_elevated_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print("Command output:", result.stdout)
        if result.stderr:
            print("Command error:", result.stderr)
        return True, []  # Success, no errors
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False, [str(e)]  # Failure, with error details

def change_root_app_pool(site_name, app_pool_name):
    command = f'%windir%\\system32\\inetsrv\\appcmd.exe set app /app.name:"{site_name}/" /applicationPool:"{app_pool_name}"'
    print(f"Changing application pool for root application of site '{site_name}' to '{app_pool_name}'...")
    return run_elevated_command(command)

def change_app_app_pool(site_name, application_name, app_pool_name):
    command = f'%windir%\\system32\\inetsrv\\appcmd.exe set app /app.name:"{site_name}/{application_name}" /applicationPool:"{app_pool_name}"'
    print(f"Changing application pool for application '{application_name}' to '{app_pool_name}'...")
    return run_elevated_command(command)

if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        success1, errors1 = change_root_app_pool(site_name, app_pool_name)
        success2, errors2 = change_app_app_pool(site_name, application_name, app_pool_name)
        # Log the results (assuming log_file and s_no are passed or managed globally)
        # Example: write_log(log_file, s_no, "Basic_settings.py", client_name, success1 and success2, not (success1 and success2), errors1 + errors2)
        print("Process completed.")