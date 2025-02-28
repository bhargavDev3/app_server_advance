import os
import glob
import subprocess
from app_main import client_name, WINRAR_PATH, base_path, log_file
from log import write_log

def delete_buildx_rar_files(folder_path):
    try:
        rar_files = glob.glob(os.path.join(folder_path, "[bB]uild*.rar"))
        for rar_file in rar_files:
            file_name = os.path.basename(rar_file)
            if file_name.lower() != "build.rar":
                os.remove(rar_file)
                print(f"Deleted: {file_name}")
            else:
                print(f"Skipped: {file_name} (protected)")
        write_log(log_file, 2, "Delete_Backup.py", client_name, 1, 0, [])  # Log success
    except Exception as e:
        print(f"An error occurred in delete_buildx_rar_files: {e}")
        write_log(log_file, 2, "Delete_Backup.py", client_name, 0, 1, [str(e)])  # Log failure

def process_folder(folder_path):
    rar_files = [f for f in os.listdir(folder_path) if f.lower().startswith("build") and f.endswith(".rar")]
    if rar_files:
        print(f"Found .rar files: {rar_files}")
        delete_buildx_rar_files(folder_path)
        build_rar_path = None
        for rar_file in rar_files:
            if rar_file.lower() == "build.rar":
                build_rar_path = os.path.join(folder_path, rar_file)
                break
        if build_rar_path:
            new_name = os.path.join(folder_path, "Build1.rar")
            os.rename(build_rar_path, new_name)
            print(f"Renamed {os.path.basename(build_rar_path)} to Build1.rar")
        else:
            print("Build.rar not found.")
        build_folder = os.path.join(folder_path, "Build")
        if os.path.exists(build_folder):
            subprocess.run([WINRAR_PATH, "a", "-r", os.path.join(folder_path, "Build.rar"), build_folder])
            print(f"Added Build folder to Build.rar")
        else:
            print("Build folder not found.")
    else:
        build_folder = os.path.join(folder_path, "Build")
        if os.path.exists(build_folder):
            subprocess.run([WINRAR_PATH, "a", "-r", os.path.join(folder_path, "Build.rar"), build_folder])
            print(f"Added Build folder to Build.rar")
        else:
            print("Build folder not found.")

folder_path = fr"{base_path}\{client_name}"
process_folder(folder_path)