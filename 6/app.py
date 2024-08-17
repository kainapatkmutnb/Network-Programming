from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, join_room, leave_room, emit
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app)

rooms = {}  # Track users in rooms

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/chat')
def chat():
    return render_template('index.html')

@app.route('/rooms')
def get_rooms():
    return jsonify(list(rooms.keys()))

@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data['room']

    if room not in rooms:
        rooms[room] = []
    rooms[room].append(username)

    join_room(room)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    emit('status', {'message': f'{username} has joined the room.', 'timestamp': timestamp}, room=room)

@socketio.on('ready-for-video')
def handle_ready_for_video(data):
    room = data['room']
    username = data['username']
    peer_id = request.sid

    emit('initiate-video', {'peerId': peer_id}, room=room, skip_sid=peer_id)

@socketio.on('video-signal')
def handle_video_signal(data):
    signal = data['signal']
    peer_id = data['peerId']

    emit('video-signal', {'signal': signal, 'peerId': request.sid}, room=peer_id)

@socketio.on('stop-video')
def handle_stop_video(data):
    room = data['room']
    emit('user-stopped-video', {'username': data['username']}, room=room)

@socketio.on('send-message')
def handle_send_message(data):
    room = data['room']
    username = data['username']
    message = data['message']
    timestamp = data['timestamp']

    emit('receive-message', {'username': username, 'message': message, 'timestamp': timestamp}, room=room)

@socketio.on('leave')
def handle_leave(data):
    username = data['username']
    room = data['room']

    leave_room(room)
    rooms[room].remove(username)
    if not rooms[room]:
        del rooms[room]

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    emit('status', {'message': f'{username} has left the room.', 'timestamp': timestamp}, room=room)

@socketio.on('disconnect')
def handle_disconnect():
    username = request.args.get('username')
    room = request.args.get('room')

    if room in rooms and username in rooms[room]:
        rooms[room].remove(username)
        if not rooms[room]:
            del rooms[room]

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        emit('status', {'message': f'{username} has disconnected.', 'timestamp': timestamp}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
