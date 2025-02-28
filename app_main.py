import os
import subprocess
import time
from log import create_log_file, write_log, close_log_file

# Common variables for all scripts
client_name = "Hallmark"      # Client name 
date = "28022025"             # Today date
app_pool_name = f"{client_name}_{date}"
site_name = client_name
application_name = "OCRWEBAPI"    # Application name under client site

# Paths
WINRAR_PATH = r"C:\Program Files\WinRAR\WinRAR.exe"
New_Build_Source = r"C:/Production_release/NewBuild_13022025/NewBuild"  # Change with New Build path
base_path = r"C:\Production2"     # Change with client base path from C drive 

# List of scripts to execute in order
scripts = [
    "iis_stop.py",
    "Delete_Backup.py",
    "Copy_paste.py",
    "Dashboard.py",
    "Ocr.py",
    "app_pool_create.py",
    "Basic_settings.py"
]

# Create log file
log_file = create_log_file(client_name, date)

# Function to run a script using subprocess
def run_script(script_name, s_no):
    try:
        print(f"Executing {script_name}...")
        result = subprocess.run(["python", script_name], check=True, text=True, capture_output=True)
        print(result.stdout)  # Print the output of the script

        # Recheck if the task was completed successfully
        if script_name == "Delete_Backup.py":
            if not check_delete_backup_completion():
                write_log(log_file, s_no, script_name, client_name, 1, 1, ["Recheck failed: Backup not deleted"])  # Log partial success
                return
        elif script_name == "Copy_paste.py":
            if not check_copy_paste_completion():
                write_log(log_file, s_no, script_name, client_name, 1, 1, ["Recheck failed: Files not copied"])  # Log partial success
                return

        # Log success
        write_log(log_file, s_no, script_name, client_name, 1, 0, [])
        print(f"{script_name} completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing {script_name}: {e.stderr}")
        write_log(log_file, s_no, script_name, client_name, 0, 1, [e.stderr])  # Log failure
        raise  # Stop execution if any script fails

# Check if Delete_Backup.py completed successfully
def check_delete_backup_completion():
    folder_path = fr"{base_path}\{client_name}"
    rar_files = [f for f in os.listdir(folder_path) if f.lower().startswith("build") and f.endswith(".rar")]
    return len(rar_files) == 1  # Only Build.rar should remain

# Check if Copy_paste.py completed successfully
def check_copy_paste_completion():
    client_path = fr"{base_path}/{client_name}/Build"
    if not os.path.exists(client_path):
        return False
    return len(os.listdir(client_path)) > 0  # Ensure files were copied

# Order of execution with delays
def execute_scripts():
    print("Starting script execution...")
    s_no = 1  # Serial number for logs

    # Step 1: Run iis_stop.py
    run_script(scripts[0], s_no)
    s_no += 1
    time.sleep(5)  # 10-second delay

    # Step 2: Run Delete_Backup.py
    run_script(scripts[1], s_no)
    s_no += 1
    time.sleep(30)  # 1.5-minute delay (90 seconds)

    # Step 3: Run Copy_paste.py
    run_script(scripts[2], s_no)
    s_no += 1
    time.sleep(120)  # 10-second delay

    # Step 4: Run Dashboard.py
    run_script(scripts[3], s_no)
    s_no += 1
    time.sleep(10)  # 10-second delay

    # Step 5: Run Ocr.py
    run_script(scripts[4], s_no)
    s_no += 1
    time.sleep(10)  # 10-second delay

    # Step 6: Run app_pool_create.py
    run_script(scripts[5], s_no)
    s_no += 1
    time.sleep(10)  # 10-second delay

    # Step 7: Run Basic_settings.py
    run_script(scripts[6], s_no)

    print("All scripts executed successfully.")
    close_log_file(log_file)  # Close the log file

# Run the scripts in order
if __name__ == "__main__":
    execute_scripts()