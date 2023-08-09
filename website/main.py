from flask import Flask, render_template, url_for, redirect, request, session, jsonify
from client import Client
from threading import Thread
import time

NAME_KEY = "name"
client = None
messages = []


app = Flask(__name__)
app.secret_key = "hello"  

@app.route("/")
@app.route("/home")
def home():
    if NAME_KEY not in session:
        return redirect(url_for("login"))
    return render_template('index.html', **{"login": True, "session": session})

def disconnect():
    global client
    if client:
        client.disconnect()

@app.route("/login", methods =["POST", "GET"])
def login():
    if request.method == "POST":
        session[NAME_KEY] = request.form["inputName"]
        global client
        client = Client(session[NAME_KEY])
        return redirect(url_for("home"))
    return render_template("login.html", **{"session": session})

@app.route("/logout")
def logout():
    disconnect()
    session.pop(NAME_KEY, None)
    return redirect(url_for("login"))

@app.route("/send_message", methods = ["GET"])
def send_message():
    global client
    msg = request.args.get("val")
    if client:
        client.send_message(msg)
    return ""  

@app.route("/get_messages")
def get_messages():
    global messages
    msg_copy = messages
    messages = []
    return msg_copy
    

def update_messages():
    global messages
    while True:
        time.sleep(0.1)
        if not client: continue
        new_msgs = client.get_messages()
        messages.extend(new_msgs)
        for msg in new_msgs:
            if(msg == "{quit}"):
                break


if __name__ == "__main__":
    Thread(target=update_messages).start()
    app.run(debug=True)
    