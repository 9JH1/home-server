import flask
import subprocess 
import os
import flask_cors
import socket
 

files_route = "static/resources/"

app = flask.Flask(__name__)
CORS = flask_cors.CORS(app)
# ROUTES
@app.route("/") 
def render_home(): 
    return flask.render_template("index.html")

@app.route("/debug")
def render_debug(): 
    return flask.render_template("debug.html")

#data points

@app.route("/files") 
def serv_files(): 
    files = os.listdir(files_route)
    file_list = []
    for file in files:
        if(len(file.split(".")) > 1):
            if((file.split("."))[1] in ["jpg","jpeg","mp4"]):
                file_list.append(f"{files_route}{file}")
    return flask.jsonify(file_list)

@app.route("/all_files")
def serv_all_files(): 
    file_list = []
    for file in os.listdir(files_route): 
        file_list.append(f"{files_route}{file}")
    return flask.jsonify(file_list)

@app.route('/resources/<path:filename>')
def serve_static(filename):
    return flask.send_from_directory('static/resources', filename)


@app.route("/info")
def serv_info():
    return f"{socket.gethostname()} | {socket.gethostbyname(socket.gethostname())}"


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