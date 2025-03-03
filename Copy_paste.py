import os
import shutil
import time
import subprocess
import ctypes
import sys
from app_main import client_name, New_Build_Source, base_path
from app_log_utils import write_log

client_path = fr"{base_path}/{client_name}/Build"
completion_flag_file = os.path.join(base_path, "copy_paste_completed.flag")

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_powershell_command(command):
    """Run a PowerShell command and return the output."""
    try:
        result = subprocess.run(["powershell", "-Command", command], check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Error: {result.stderr}")
        return True, []
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute PowerShell command: {e.stderr}")
        return False, [str(e)]

def update_timestamp(path):
    """Update the last modified timestamp of a file or folder."""
    current_time = time.time()
    os.utime(path, (current_time, current_time))
    return True, []

def clean_directory(client_path):
    """Delete all folders and files in client_path except MailContent folder and Web.config file."""
    if not os.path.exists(client_path):
        print(f"The path {client_path} does not exist.")
        return False, [f"Path {client_path} does not exist."]
    for item in os.listdir(client_path):
        item_path = os.path.join(client_path, item)
        if item == "MailContent" or item == "Web.config":
            print(f"Skipping {item}")
            continue
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                # Use PowerShell to forcefully delete the file
                success, errors = run_powershell_command(f"Remove-Item -Path '{item_path}' -Force")
                if not success:
                    return False, errors
                print(f"Deleted file: {item}")
            elif os.path.isdir(item_path):
                # Use PowerShell to forcefully delete the folder
                success, errors = run_powershell_command(f"Remove-Item -Path '{item_path}' -Recurse -Force")
                if not success:
                    return False, errors
                print(f"Deleted folder: {item}")
        except Exception as e:
            print(f"Failed to delete {item}. Reason: {e}")
            return False, [str(e)]
    return True, []

def copy_except_excluded(New_Build_Source, client_path):
    """Copy all folders and files from New_Build_Source to client_path except MailContent folder and Web.config file."""
    if not os.path.exists(New_Build_Source):
        print(f"Source path {New_Build_Source} does not exist.")
        return False, [f"Source path {New_Build_Source} does not exist."]
    if not os.path.exists(client_path):
        print(f"Destination path {client_path} does not exist.")
        return False, [f"Destination path {client_path} does not exist."]
    for item in os.listdir(New_Build_Source):
        source_item_path = os.path.join(New_Build_Source, item)
        destination_item_path = os.path.join(client_path, item)
        if item == "MailContent" or item == "Web.config":
            print(f"Skipping {item}")
            continue
        try:
            if os.path.isfile(source_item_path):
                shutil.copy2(source_item_path, destination_item_path)
                print(f"Copied file: {item}")
            elif os.path.isdir(source_item_path):
                shutil.copytree(source_item_path, destination_item_path)
                print(f"Copied folder: {item}")
            update_timestamp(destination_item_path)
            print(f"Updated timestamp for: {item}")
        except Exception as e:
            print(f"Failed to copy {item}. Reason: {e}")
            return False, [str(e)]
    return True, []

def execute_copy_paste_process():
    """Execute the entire copy-paste process."""
    print("Executing Copy_paste.py...")

    # Step 1: Clean client_path
    print("Step 1: Cleaning client_path...")
    success, errors = clean_directory(client_path)
    if not success:
        # Log the failure
        # Example: write_log(log_file, s_no, "Copy_paste.py", client_name, success, not success, errors)
        sys.exit(1)
    time.sleep(5)

    # Step 2: Copy from New_Build_Source to client_path
    print("\nStep 2: Copying from New_Build_Source to client_path...")
    success, errors = copy_except_excluded(New_Build_Source, client_path)
    if not success:
        # Log the failure
        # Example: write_log(log_file, s_no, "Copy_paste.py", client_name, success, not success, errors)
        sys.exit(1)

    # Create a completion flag file
    with open(completion_flag_file, "w") as flag_file:
        flag_file.write("Copy_paste.py completed successfully.")

    # Log the success
    # Example: write_log(log_file, s_no, "Copy_paste.py", client_name, success, not success, errors)
    print("\nCopy_paste.py completed successfully.")

if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        execute_copy_paste_process()