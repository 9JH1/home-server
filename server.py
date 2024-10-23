import flask
import subprocess 
import os
import flask_cors
import socket
import time
import math
import psutil
import shutil


files_route = "/home/_3hy/.FILE_WARD/favorites" # full path
#files_route = "/home/_3hy/.steam/steam/steamapps/compatdata/244210/pfx/drive_c/users/steamuser/Documents/Assetto Corsa/screens"
#files_route = "/home/_3hy/Downloader/downloads/General Searchs/"
ver ="8"
app = flask.Flask(__name__)
CORS = flask_cors.CORS(app)

# ROUTES
@app.route("/") 
def render_home(): 
    return flask.render_template("index.html")
#data points

@app.route("/fix")
def render_fix():
    files_route = "/home/_3hy"
    return "yes sir"
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
