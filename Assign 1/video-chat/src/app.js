const express = require('express');
const app = express();
const server = require('http').createServer(app);
const io = require('socket.io')(server);
const stream = require('./ws/stream');
const path = require('path');

// Serve static assets from the 'assets' directory
app.use('/assets', express.static(path.join(__dirname, 'assets')));

// Serve the index.html file at the root URL
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Set up the '/stream' namespace and attach the stream handler
io.of('/stream').on('connection', stream);

// Start the server and listen on port 3000
server.listen(3000, () => {
  console.log('Server listening on port 3000');
});