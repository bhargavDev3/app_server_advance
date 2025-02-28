import subprocess
import ctypes
import sys
from app_main import client_name, site_name, application_name, app_pool_name, log_file
from log import write_log

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
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False

def change_root_app_pool(site_name, app_pool_name):
    command = f'%windir%\\system32\\inetsrv\\appcmd.exe set app /app.name:"{site_name}/" /applicationPool:"{app_pool_name}"'
    print(f"Changing application pool for root application of site '{site_name}' to '{app_pool_name}'...")
    if run_elevated_command(command):
        print(f"Successfully changed application pool for root application of site '{site_name}'.")
        write_log(log_file, 7, "Basic_settings.py", client_name, 1, 0, [])  # Log success
    else:
        print(f"Failed to change application pool for root application of site '{site_name}'.")
        write_log(log_file, 7, "Basic_settings.py", client_name, 0, 1, [])  # Log failure

def change_app_app_pool(site_name, application_name, app_pool_name):
    command = f'%windir%\\system32\\inetsrv\\appcmd.exe set app /app.name:"{site_name}/{application_name}" /applicationPool:"{app_pool_name}"'
    print(f"Changing application pool for application '{application_name}' to '{app_pool_name}'...")
    if run_elevated_command(command):
        print(f"Successfully changed application pool for application '{application_name}'.")
        write_log(log_file, 7, "Basic_settings.py", client_name, 1, 0, [])  # Log success
    else:
        print(f"Failed to change application pool for application '{application_name}'.")
        write_log(log_file, 7, "Basic_settings.py", client_name, 0, 1, [])  # Log failure

if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        change_root_app_pool(site_name, app_pool_name)
        change_app_app_pool(site_name, application_name, app_pool_name)
        print("Process completed.")