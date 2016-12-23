from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def rootRoute():
	return render_template('index.html')

@socketio.on('my event')
def handle_my_custom_event(json):
	print('received json: ' + str(json))

def start():
	socketio.run(app)
