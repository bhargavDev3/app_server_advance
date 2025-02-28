import os
import datetime

# Log file configuration
LOG_DIR = "logs"  # Logs will be saved in the "logs" directory inside the current directory
os.makedirs(LOG_DIR, exist_ok=True)

def create_log_file(client_name, date):
    """Creates a new log file with the given client name and date."""
    # Generate the base log file name
    base_log_file = f"{client_name}_{date.replace('/', '_')}.html"
    log_file = os.path.join(LOG_DIR, base_log_file)

    # Create the log file with the HTML structure
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Deployment Logs - {client_name} - {date}</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css" rel="stylesheet">
        <style>
            body {{
                background: #ffffff;
                font-family: 'Arial', sans-serif;
                color: #333333;
            }}
            .table-container {{
                background: #ffffff;
                border-radius: 15px;
                padding: 20px;
                margin: 20px auto;
                max-width: 1200px;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(0, 0, 0, 0.1);
            }}
            .table-header {{
                background: #f8f9fa;
                color: #333333;
                font-weight: bold;
            }}
            .table-row {{
                background: #ffffff;
                transition: background 0.3s ease;
            }}
            .table-row:hover {{
                background: #f8f9fa;
            }}
            .failed-link {{
                color: #ff6b6b;
                text-decoration: underline;
            }}
            .failed-link:hover {{
                color: #ff4757;
            }}
            .success {{
                color: #4cd137;
            }}
            .failure {{
                color: #ff4757;
            }}
            .fade-in {{
                animation: fadeIn 0.5s ease-in;
            }}
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
            h1 {{
                color: #333333;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
            }}
        </style>
    </head>
    <body class="p-8">
        <div class="table-container animate__animated animate__fadeIn">
            <h1 class="text-4xl font-bold text-center mb-8">
                Deployment Logs - <span class="text-blue-600">{client_name}</span> - <span class="text-purple-600">{date}</span>
            </h1>
            <table class="min-w-full">
                <thead class="table-header">
                    <tr>
                        <th class="py-4 px-6 text-left">S-No</th>
                        <th class="py-4 px-6 text-left">Date</th>
                        <th class="py-4 px-6 text-left">Execution Type</th>
                        <th class="py-4 px-6 text-left">Client-Name</th>
                        <th class="py-4 px-6 text-left">Successful</th>
                        <th class="py-4 px-6 text-left">Failed</th>
                        <th class="py-4 px-6 text-left">Paths_failed</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-200">
    """
    with open(log_file, "w", encoding="utf-8") as file:
        file.write(html_content)
    return log_file

def write_log(log_file, s_no, execution_type, client_name, successful, failed, paths_failed):
    """Writes a log entry to the log file."""
    # Format failed paths as clickable links
    failed_links = "<br>".join([f'<a href="{path}" class="failed-link">{path}</a>' for path in paths_failed])

    log_entry = f"""
    <tr class="table-row fade-in">
        <td class="py-4 px-6 border-b">{s_no}</td>
        <td class="py-4 px-6 border-b">{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td>
        <td class="py-4 px-6 border-b">{execution_type}</td>
        <td class="py-4 px-6 border-b">{client_name}</td>
        <td class="py-4 px-6 border-b success">{successful}</td>
        <td class="py-4 px-6 border-b failure">{failed}</td>
        <td class="py-4 px-6 border-b">{failed_links}</td>
    </tr>
    """
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(log_entry)

def close_log_file(log_file):
    """Closes the log file by adding the closing HTML tags."""
    with open(log_file, "a", encoding="utf-8") as file:
        file.write("""
                </tbody>
            </table>
        </div>
    </body>
    </html>
        """)