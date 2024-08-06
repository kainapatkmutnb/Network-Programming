const express = require('express');
const app = express();
const http = require('http').createServer(app);
const io = require('socket.io')(http);

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', (socket) => {
  console.log('a user connected');
  socket.on('disconnect', () => {
    console.log('user disconnected');
  });
  socket.on('chat message', (msg) => {
    socket.emit('chat message', msg); // ส่งข้อความกลับไปยังไคลเอนต์ที่ส่งข้อความมา
  });
});

http.listen(3000, () => {
  console.log('listening on *:3000');
});