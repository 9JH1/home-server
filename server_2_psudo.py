import flask
import flask_cors
import os
from hashlib import sha256
from sys import argv
from base64 import b64decode, b64encode
from mimetypes import guess_type
from io import BytesIO

# start vars
route="/drive"
route_favorites = "/drive/favorites"
secure_path=0
try:
    route=argv[1]
except:
    print("",end="")
server_password = "75e9bc89514d1b8ca251cbd922500acee7dd102922cb4e671e9dbdf63cbbdd8c"

# flask init
app = flask.Flask(__name__)
CORS = flask_cors.CORS(app)

@app.route(f"/{server_password}/route")
def return_route():
    return route

def encrypt_string(hash_string):
    return sha256(hash_string.encode()).hexdigest()

@app.route(f"/{server_password}/lsdir/<path:dirl>")
def list_dir(dirl):
    # if the path is out of bounds stop the request
    if route in dirl or secure_path==0:
        if not dirl.startswith("/"):
                dirl = "/" + dirl
        # if the path is in the request then continue
        file_list = {}
        for file in os.listdir(dirl):
            file_list[file] = os.path.isdir(os.path.join(dirl,file))
        return flask.jsonify(file_list)

    else:
        return flask.Response("Path Forbidden",status=403)

@app.route(f"/<server_password>/lsdirr/<path:dirl>")
def list_dir_recurse(server_password, dirl):
    if route in dirl or secure_path == 0:
        if not dirl.startswith("/"): dirl = "/" + dirl
        file_list = {}

        def recurse(dirl):
            try:
                for file in os.listdir(dirl):
                    file_path = os.path.join(dirl, file)
                    if os.path.isdir(file_path):
                        recurse(file_path)
                    else:
                        file_list[file_path] = False
            except:
                pass

        recurse(dirl)
        return flask.jsonify(file_list)
    return flask.Response("Path Forbidden", status=403)

@app.route(f"/{server_password}/fetch/<path:dirl>")
def serve_file(dirl):
    if route in dirl or secure_path==0:
        try:
            if not dirl.startswith("/"):
                dirl = "/" + dirl
            with open(dirl,"rb") as file:
                data = file.read()
                mime, _ = guess_type(dirl)
                if mime is None:
                    mime = "application/octet-stream"
                return flask.Response(BytesIO(data), mimetype=mime)
        except Exception as e:
            return flask.Response(f"Error serving file: {str(e)}", status=500)
    else:
        return flask.Response("Path Forbidden",status=403)
@app.route("/")
def render_base():
    return flask.render_template("iid.html")

@app.route(f"/{server_password}/setfav/<path:dirl>")
def set_favorite(dirl):
    if route in dirl or not secure_path:
        if not dirl.startswith("/"):
            dirl = "/" + dirl
        symlink_path = os.path.join(route_favorites, os.path.basename(dirl))
        
        try:
            if not os.path.exists(symlink_path):
                os.symlink(dirl, symlink_path)
            return flask.Response(status=200)
        except Exception as e:
            return flask.Response(str(e), status=500)
    else:
        return flask.Response("Path Forbidden", status=403)

@app.route(f"/{server_password}/chkfav/<path:dirl>")
def chk_favorite(dirl):
    if route in dirl or not secure_path:
        if not dirl.startswith("/"):
            dirl = "/" + dirl
        symlink_path = os.path.join(route_favorites, os.path.basename(dirl))
        
        if os.path.exists(symlink_path):
            return "true"
        else:
            return "false"
    else:
        return flask.Response("Path Forbidden", status=403)

@app.route(f"/{server_password}/remfav/<path:dirl>")
def rem_favorite(dirl):
    if route in dirl or not secure_path:
        if not dirl.startswith("/"):
            dirl = "/" + dirl
        symlink_path = os.path.join(route_favorites, os.path.basename(dirl))
        
        try:
            if os.path.exists(symlink_path) and os.path.islink(symlink_path):
                os.unlink(symlink_path)
                return "true"
            else:
                return "false"
        except Exception as e:
            return flask.Response(str(e), status=500)
    else:
        return flask.Response("Path Forbidden", status=403)
if __name__ == "__main__":
    app.run(port=3031,host="0.0.0.0") 