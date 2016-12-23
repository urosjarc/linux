from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def rootRoute():
	return render_template('index.html')

@socketio.on('my event')
def handle_my_custom_event(json):
	print('received json: ' + str(json))

@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
	print(e)

@socketio.on('connect')
def client_connect():
	print('Client connected')

@socketio.on('disconnect')
def client_disconnect():
	print('Client disconnected')

def start():
	socketio.run(app)
