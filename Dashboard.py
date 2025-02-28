import re
import os
import subprocess
import ctypes
import sys
from app_main import client_name, base_path, log_file
from log import write_log

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def find_correct_case_path(base_path, client_name):
    """Find the correct case of the client_name in the base path."""
    if os.path.exists(base_path):
        for dir_name in os.listdir(base_path):
            if dir_name.lower() == client_name.lower():
                return os.path.join(base_path, dir_name)
    raise FileNotFoundError(f"Directory for client '{client_name}' not found in '{base_path}'")

def modify_file_content(file_path, client_name):
    """Modify the content of the file."""
    try:
        # Read the content of the file
        with open(file_path, 'r') as file:
            content = file.read()

        # Step 1: Replace any api_server_ip value with the desired one
        content = re.sub(r'var api_server_ip = "https://[^"]+";', 
                         r'var api_server_ip = "https://dashboardapi.nimbleproperty.net";', 
                         content)

        # Step 2: Replace any client value with the provided client_name
        content = re.sub(r'var client = "[^"]+";', 
                         f'var client = "{client_name}";', 
                         content)

        # Write the modified content back to the file
        with open(file_path, 'w') as file:
            file.write(content)

        print(f"File '{file_path}' has been updated successfully.")
        write_log(log_file, 4, "Dashboard.py", client_name, 1, 0, [])  # Log success
    except Exception as e:
        print(f"Failed to update file '{file_path}'. Reason: {e}")
        write_log(log_file, 4, "Dashboard.py", client_name, 0, 1, [str(e)])  # Log failure

def main():
    # Find the correct case of the client_name in the base path
    client_path = find_correct_case_path(base_path, client_name)

    # Define the paths to the files using the correct case of client_name
    dashboard_new_path = os.path.join(client_path, "Build", "Dashboard_New", "js", "dashboard_New.js")
    dashboard_new_chart_path = os.path.join(client_path, "Build", "Dashboard_New", "js", "Dashboard_NewCharts.js")

    # Modify both files
    modify_file_content(dashboard_new_path, client_name)
    modify_file_content(dashboard_new_chart_path, client_name)

# Check if the script is running as administrator
if not is_admin():
    # Request admin privileges if not already running as admin
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
else:
    # Run the main script if running as admin
    main()