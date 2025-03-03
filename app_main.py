import subprocess
import time
import os
from app_log_utils import create_log_file, write_log, close_log_file

# Common variables for all scripts
client_name = "Hallmark"  # Client name
date = "53022025"  # Today date
app_pool_name = f"{client_name}_{date}"
site_name = client_name
application_name = "OCRWEBAPI"  # Application name under client site

# Paths
WINRAR_PATH = r"C:\Program Files\WinRAR\WinRAR.exe"
New_Build_Source = r"C:/Production_release/NewBuild_13022025/NewBuild"  # Change with New Build path
base_path = r"C:\Production1"  # Change with client base path from C drive
completion_flag_file = os.path.join(base_path, "copy_paste_completed.flag")

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

# Function to run a script using subprocess
def run_script(script_name, log_file, s_no):
    try:
        print(f"Executing {script_name}...")
        # Run the script
        process = subprocess.Popen(["python", script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait for the process to complete
        stdout, stderr = process.communicate()
        
        # Print the output of the script
        print(stdout)
        if stderr:
            print(f"Errors in {script_name}: {stderr}")
        
        # Check if the process completed successfully
        if process.returncode == 0:
            print(f"{script_name} completed successfully.")
            write_log(log_file, s_no, script_name, client_name, 1, 0, [])
        else:
            print(f"{script_name} failed with return code {process.returncode}.")
            write_log(log_file, s_no, script_name, client_name, 0, 1, [stderr])
            raise subprocess.CalledProcessError(process.returncode, script_name, stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing {script_name}: {e.stderr}")
        write_log(log_file, s_no, script_name, client_name, 0, 1, [str(e)])
        raise  # Stop execution if any script fails

# Order of execution with delays
def execute_scripts():
    print("Starting script execution...")

    # Create the log file
    log_file = create_log_file(client_name, date)
    s_no = 1

    # Step 1: Run iis_stop.py
    run_script(scripts[0], log_file, s_no)
    s_no += 1
    time.sleep(10)  # 5-second delay

    # Step 2: Run Delete_Backup.py
    run_script(scripts[1], log_file, s_no)
    s_no += 1
    time.sleep(10)  # 1-minute delay

    # Step 3: Run Copy_paste.py
    run_script(scripts[2], log_file, s_no)
    s_no += 1

    # Wait for the completion flag file
    while not os.path.exists(completion_flag_file):
        time.sleep(1)  # Wait for 1 second before checking again
    print("Copy_paste.py completed successfully.")
    os.remove(completion_flag_file)  # Clean up the flag file
    time.sleep(10)
    # Step 4: Run Dashboard.py
    run_script(scripts[3], log_file, s_no)
    s_no += 1
    time.sleep(10)  # 10-second delay

    # Step 5: Run Ocr.py
    run_script(scripts[4], log_file, s_no)
    s_no += 1
    time.sleep(10)  # 10-second delay

    # Step 6: Run app_pool_create.py
    run_script(scripts[5], log_file, s_no)
    s_no += 1
    time.sleep(10)  # 10-second delay

    # Step 7: Run Basic_settings.py
    run_script(scripts[6], log_file, s_no)

    # Close the log file
    close_log_file(log_file)
    print("All scripts executed successfully.")

# Run the scripts in order
if __name__ == "__main__":
    execute_scripts()