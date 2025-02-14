
const tls = require('tls');
const fs = require('fs');
const url = require('url');

var msg = 'welcome!';
const localhost = "127.0.0.1";
const options = {
  key: fs.readFileSync('server-key.pem'),
  cert: fs.readFileSync('server-cert.pem'),

  rejectUnauthorized: true,
};

const server = tls.createServer(options, (socket) => {
  console.log('server connected',
              socket.authorized ? 'authorized' : 'unauthorized');
  url.parse(msg)
  socket.write(msg);
  socket.setEncoding('utf8');
  socket.pipe(socket);
});
server.listen(8000, () => {
  console.log('server bound');
});
server.listen(localhost, () => {
  console.log('server bound');
});
