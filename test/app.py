from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

rooms = {}

def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rooms')
def get_rooms():
    return jsonify(list(rooms.keys()))

@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    if room not in rooms:
        rooms[room] = []
    rooms[room].append(username)
    timestamp = get_timestamp()
    emit('status', {'message': f'[{timestamp}] {username} has joined the room.'}, room=room)

@socketio.on('leave')
def handle_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    rooms[room].remove(username)
    timestamp = get_timestamp()
    emit('status', {'message': f'[{timestamp}] {username} has left the room.'}, room=room)

@socketio.on('message')
def handle_message(data):
    username = data['username']
    room = data['room']
    message = data['message']
    timestamp = get_timestamp()
    emit('message', {'username': username, 'message': message, 'timestamp': timestamp}, room=room)

@socketio.on('video-offer')
def handle_video_offer(data):
    emit('video-offer', data, room=data['room'])

@socketio.on('video-answer')
def handle_video_answer(data):
    emit('video-answer', data, room=data['room'])

@socketio.on('video-candidate')
def handle_video_candidate(data):
    emit('video-candidate', data, room=data['room'])

@socketio.on('video-stop')
def handle_video_stop(data):
    emit('video-stop', data, room=data['room'])

if __name__ == '__main__':
    socketio.run(app, debug=True)
