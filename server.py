ver = "8"
import flask
import subprocess 
import os
import flask_cors
import socket
import time
import math
import psutil
import shutil
import requests
files_route = "/home/_3hy/Pictures/" # full path
#files_route = "/home/_3hy/.steam/steam/steamapps/compatdata/244210/pfx/drive_c/users/steamuser/Documents/Assetto Corsa/screens"
#files_route = "/home/_3hy/Downloader/downloads/General Searchs/"
app = flask.Flask(__name__)
CORS = flask_cors.CORS(app)

@app.route("/latest_version_update_check")
def fetch_first_line():
    url = "https://raw.githubusercontent.com/9jh1/home-server/refs/heads/main/server.py"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        first_line = response.text.splitlines()[0]  # Get the first line


        return first_line.split("=")[1]
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

# ROUTES
@app.route("/") 
def render_home(): 
    return flask.render_template("index.html")
#data points

@app.route("/files")
def list_files():
    result = []
    for root, dirs, files in os.walk(files_route):
        for file in files:
            result.append(os.path.join(root, file).replace(files_route,""))
    return flask.jsonify(result)  # Use jsonify to return a list of full file paths

@app.route('/<path:filename>')
def serve_static(filename):
    return flask.send_from_directory(files_route, filename)

def get_ping():
    try:
        result = subprocess.run(['ping', '-c', '1', socket.gethostbyname(socket.gethostname())], capture_output=True, text=True, timeout=10)
        ping_time = result.stdout.split("time=")[1].split(" ")[0]
        return str(ping_time)
    except (IndexError, subprocess.TimeoutExpired):
        return None
@app.route("/query_database_files/<index>")
def query_database_files(index):
    folder_info = []
    result = []
    # Check if the provided path exists and is a directory
    if os.path.exists(files_route) and os.path.isdir(files_route):
        for folder_name in os.listdir(files_route):
            folder_path = os.path.join(files_route, folder_name)
            
            # Check if it is a directory
            if os.path.isdir(folder_path):
                folder_size = get_folder_size(folder_path)
                folder_info.append({
                    "name": folder_name,
                    "size": folder_size,
                    "path": folder_path
                })
    path = folder_info[int(index)]["path"];
    for root, dirs, files in os.walk(path):
        for file in files:
            result.append(os.path.join(root, file).replace(files_route,""))
    return flask.jsonify(result)  # Use jsonify to return a list of full file paths

@app.route("/database")
def get_folder_info():
    folder_info = []
    
    # Check if the provided path exists and is a directory
    if os.path.exists(files_route) and os.path.isdir(files_route):
        for folder_name in os.listdir(files_route):
            folder_path = os.path.join(files_route, folder_name)
            
            # Check if it is a directory
            if os.path.isdir(folder_path):
                folder_size = get_folder_size(folder_path)
                folder_info.append({
                    "name": folder_name,
                    "size": folder_size,
                    "path": folder_path
                })
    
    return flask.jsonify(folder_info)

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    
    return format_size(total_size)

def format_size(size_bytes):
    """Convert bytes to a human-readable format."""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    index = 0
    while size_bytes >= 1024 and index < len(size_names) - 1:
        size_bytes /= 1024.0
        index += 1
    
    return f"{size_bytes:.2f} {size_names[index]}"

@app.route("/info_packet")
def info_packet():
    return flask.jsonify({
        "uptime": str(time.time() - psutil.boot_time()),
        "cpu":str(psutil.cpu_percent()),
        "ram":str(psutil.virtual_memory().percent), 
        "hostname":socket.gethostname(),
        "ip":socket.gethostbyname(socket.gethostname()),
        "ping": get_ping()
    })

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in flask.request.files:
        return 'No file part'
    file = flask.request.files['file']
    if file.filename == '':
        return 'No selected file'
    # Save the file to the uploads directory
    file.save(files_route + '/' + file.filename)
    return 'File uploaded successfully'
@app.route("/version")
def version_g(): 
    return ver
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4040)
