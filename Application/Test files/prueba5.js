
var xss = require("xss");
const zlib = require('zlib');
const http2 = require('http2');
const buffer = Buffer.alloc(5);

const server = http2.createServer((req, res) => {
	// Añadimos una url al servidor, que devuelve un Hola Mundo!
	let html = xss(req.url)
	if(req.url === "/"){
		var length = buffer.write('abcd', 8);
 		res.write("Hola Mundo!"+String(html)+String(length));
		res.end();
	}
	if(req.url === "/zlib"){
  response.writeHead(200, { 'content-encoding': 'gzip' });
  var length = buffer.fill("n");
  const output = zlib.createGzip();
  let i;

  pipeline(output, response, (err) => {
    if (err) {
      // If an error occurs, there's not much we can do because
      // the server has already sent the 200 response code and
      // some amount of data has already been sent to the client.
      // The best we can do is terminate the response immediately
      // and log the error.
      clearInterval(i);
      response.end();
      console.error('An error occurred:', err);
    }
  });

  i = setInterval(() => {
    output.write(`The current time is ${Date()}\n`, () => {
      // The data has been passed to zlib, but the compression algorithm may
      // have decided to buffer the data for more efficient compression.
      // Calling .flush() will make the data available as soon as the client
      // is ready to receive it.
      output.flush();
    });
  }, 1000);



}
});

