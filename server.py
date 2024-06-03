import flask
import subprocess 
import os
import flask_cors
import socket
import time
import math
import psutil
import shutil
files_route = "static/resources/"

app = flask.Flask(__name__)
CORS = flask_cors.CORS(app)
# ROUTES
@app.route("/") 
def render_home(): 
    return flask.render_template("index.html")
#data points

@app.route("/files") 
def list_files(start_path):
    result = {}
    for root, dirs, files in os.walk(start_path):
        current_dir = result
        folders = root.split(os.sep)[1:]
        for folder in folders:
            if folder not in current_dir:
                current_dir[folder] = {}
            current_dir = current_dir[folder]
        for file in files:
            current_dir[file] = None
    return result

@app.route('/<path:filename>')
def serve_static(filename):
    return flask.send_from_directory('static/resources', filename)

@app.route("/info_name")
def serv_info_name():
    return socket.gethostname()

@app.route("/info_ip")
def serv_info_ip():
    return socket.gethostbyname(socket.gethostname())


@app.route("/ping")
def get_ping():
    try:
        result = subprocess.run(['ping', '-c', '1', 'google.com'], capture_output=True, text=True, timeout=10)
        ping_time = result.stdout.split("time=")[1].split(" ")[0]
        return str(ping_time)
    except (IndexError, subprocess.TimeoutExpired):
        return None

@app.route("/storage")
def serv_storage():
    def get_full_size():
        return shutil.disk_usage("/").total
    
    def get_used_space():
        return get_size_of_dir()
    
    def get_size_of_dir(start_path = '.'):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)

        return total_size
    
    total_space = get_full_size()
    used_space = get_used_space()
    
    if total_space == 0:
        percentage_used = 0
    else:
        percentage_used = (used_space / total_space) * 100
    
    return str(round(percentage_used, 2))




@app.route("/ram")
def serv_ram():
    return str(psutil.virtual_memory().percent)






@app.route("/uptime")
def seconds_elapsed():
    return str(time.time() - psutil.boot_time())

@app.route("/cpu")
def serv_cpu():
    return str(psutil.cpu_percent())
@app.route("/temp")
def serv_temp(): 
    data = psutil.sensors_temperatures(fahrenheit=False)
    cpu_temps = []
    for sensor, readings in data.items():
        if "coretemp" in sensor.lower() or "cpu" in sensor.lower():
            for reading in readings:
                print(f"{sensor}: {reading.current}°C")
                cpu_temps.append(reading.current)
    for sensor, readings in data.items():
        if not any(x in sensor.lower() for x in ["coretemp", "cpu"]):
            for reading in readings:
                print(f"{sensor}: {reading.current}°C")

    cpu_total = 0 
    for value in cpu_temps:
        cpu_total += value
    cpu_average = cpu_total/len(cpu_temps)
    return str(cpu_average)

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
@app.route('/delete/<path:file_path>')
def delete_file(file_path):
    try:
        os.remove(file_path)
        return "file deleted"
    except: 
        return "file does not exist"
if __name__ == "__main__":
    print("hello world")
    app.run(host="0.0.0.0")