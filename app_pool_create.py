import iis_bridge.pool as pool
import subprocess
import ctypes
import sys
from app_main import client_name, date, app_pool_name
from log_utils import write_log

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def configure_app_pool():
    try:
        if not pool.exists(app_pool_name):
            pool.create(app_pool_name)
            print(f"Application Pool {app_pool_name} created successfully.")
        else:
            print(f"Application Pool {app_pool_name} already exists.")
        pool.config(app_pool_name, thirty_two_bit=True)
        pool.config(app_pool_name, idle_timeout="24:00:00")
        pool.config(app_pool_name, recycle_after_time="00:00:00")
        pool.config(app_pool_name, recycle_at_time="02:00:00")
        print(f"Application Pool {app_pool_name} configured successfully.")
        return True, []  # Success, no errors
    except Exception as e:
        print(f"An error occurred while configuring the application pool: {e}")
        return False, [str(e)]  # Failure, with error details

if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        success, errors = configure_app_pool()
        # Log the result (assuming log_file and s_no are passed or managed globally)
        # Example: write_log(log_file, s_no, "app_pool_create.py", client_name, success, not success, errors)