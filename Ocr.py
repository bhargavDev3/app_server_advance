import re
import os
import subprocess
import ctypes
import sys
from app_main import client_name, base_path
from log_utils import write_log

client_site = f"https://{client_name}.nimbleproperty.net"

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

def replace_apiurl(content):
    """Replace the apiurl with the client_site."""
    pattern = r"var apiurl = '[^']*';"
    replacement = f"var apiurl = '{client_site}/OCRWEBAPI/api';"
    return re.sub(pattern, replacement, content)

def replace_host(content):
    """Replace the host with the client_site."""
    pattern = r"var host = '[^']*';"
    replacement = f"var host = '{client_site}';"
    return re.sub(pattern, replacement, content)

def process_file(file_path):
    """Process a file and update its content."""
    try:
        # Read the content of the file
        with open(file_path, 'r') as file:
            content = file.read()

        # Perform the replacements
        content = replace_apiurl(content)
        content = replace_host(content)

        # Write the modified content back to the file
        with open(file_path, 'w') as file:
            file.write(content)

        print(f"File '{file_path}' has been updated successfully.")
        return True, []  # Success, no errors
    except Exception as e:
        print(f"Failed to update file '{file_path}'. Reason: {e}")
        return False, [str(e)]  # Failure, with error details

if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        # Find the correct case of the client_name in the base path
        client_path = find_correct_case_path(base_path, client_name)

        # Define the paths to the OCR files using the correct case of client_name
        OCR_management = os.path.join(client_path, "Build", "OCR", "OCRManagement.js")
        OCR_mapping = os.path.join(client_path, "Build", "OCR", "OCRFiles", "Scripts", "Mapping.js")

        # Process both files
        success1, errors1 = process_file(OCR_management)
        success2, errors2 = process_file(OCR_mapping)

        # Log the results (assuming log_file and s_no are passed or managed globally)
        # Example: write_log(log_file, s_no, "Ocr.py", client_name, success1 and success2, not (success1 and success2), errors1 + errors2)