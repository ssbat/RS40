# -*- coding: utf-8

from flask import *
import bcrypt
# définir le message secret
RESOURCES_DIR = "resources/"
SERVER_PRIVATE_KEY_FILENAME = RESOURCES_DIR + "server-private-key.pem"
SERVER_PUBLIC_KEY_FILENAME = RESOURCES_DIR + "server-public-key.pem"
SECRET_MESSAGE = "RS40 IS THE BEST UV" # A modifier
username="admin"
password="rs40"
hashed_password=bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt())
app = Flask(__name__)
@app.route("/",methods=['GET','POST'])
def get_secret_message():

    error=''
    if request.method=="POST":
        if request.form['username']!=username or not bcrypt.checkpw(request.form["password"].encode('utf-8'),hashed_password):
            error="invalid"
        else:
            return render_template("home.html",secret_message=SECRET_MESSAGE)       
            
    return render_template("index.html",error=error)

if __name__ == "__main__":

    # HTTP version
    # app.run(debug=True, host="127.0.0.1", port=8081)
    # HTTPS version; Il faut que l'on utilise le terminal ici(tapez: py run_server.py)
    context = (SERVER_PUBLIC_KEY_FILENAME,SERVER_PRIVATE_KEY_FILENAME)
    app.run(debug=True, host="127.0.0.1", port=8081, ssl_context=context)
    
    
