
const sanitize = require('google-caja-sanitizer').sanitize;

// url se encarga en el codigo de obtener los parametros de la llamada GET
const url = require('url');

const http = require('http');
// fs se encarga de leer los ficheros html, en este caso solo 1 para poder enviarlo con las funciones de http
const fs = require('fs');

const low = require('lowdb')
const FileSync = require('lowdb/adapters/FileSync')

// Esta parte de codigo me genero el json, imagino que se encarga de gestionarlo porque hay un archivo "package-lock"
const adapter = new FileSync('db.json')
const db = low(adapter)

// Esta biblioteca se encarga de tratar un string usando las funciones de DOM de javascript. Es decir
// primero leemos el archivo con fs y lo almacenamos en un String, pero con ese string no podemos hacer
// llamadas a funciones de javascript como document.getElementById, pues con esta biblioteca podemos hacerlo.
// NOTA: no lo he comprobado, creo que usa exclusivamente las llamadas "document.getElementById" que utiliza JQuery, por lo que
// si queremos usar un 'document.getElementById(ejemplo)' tendremos que usar '$("#ejemplo")'
const cheerio = require('cheerio')

const hostname = '127.0.0.1';
const port = 3000;

http.maxSockets = 10;
http.maxHeaderSize = 16;

const server = http.createServer((req, res) => {
  req.setSocketKeepAlive();
	// Añadimos una url al servidor, que devuelve un Hola Mundo!
	if(req.url === "/"){
  res.setTimeout(200);
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.writeHead(200, { 'Content-Type': 'text/plain',
                          'Trailer': 'Content-MD5' });
  res.write("Hola Mundo!");
	res.end();
	}
	
	// Añadimos la url seminarios para manejar el html que teniamos
	if(req.url === "/seminarios"){
		// leemos el archivo con fs
		fs.readFile('seminarios.html', 'utf8', function(err, data) {
		if (err) throw err;
		// Si no ha habido ningun error tenemos que obtener los datos de los seminarios y poner la nota guardada en la BD
		else {
			
			// Cargamos la funcionalidad de cheerio
			const $ = cheerio.load(data);
			console.log("Respondiendo peticion");
			// Obtenemos todos los seminarios de la pagina html(si se modifica el numero de seminarios es posible que no funcione correctamente.
			let seminarios = $('.seminario').each( function(){
				// Obtenems el id porque los elementos con clase seminario tienen como texto el id al que pertenecen
				// Cuidado que obtenemos un valor String y nosotros guardamos valores int, tenemos que convertirlo
					let id = parseInt($(this).text());
					
					// mensaje de depuracion, intente usar el this directamente pero no funcionaba no se por que
					console.log("1 :"+$(this).text() + "real "+id);
					
					// Como sabemos el id podemos obtener los datos de la BD
					let utilidad = db.get("seminarios").find({ "id": id }).get("utilidad");
					let calidad = db.get("seminarios").find({ "id": id }).get("calidad");
					
					// Mensaje de depuracion
					console.log("Seminario "+id+" utilidad "+utilidad+" calidad "+calidad);
					
					// Insertamos en la pagina los valores obtenidos de la BD
					$("#utilidad"+id).attr('value', utilidad);
					$("#calidad"+id).attr('value', calidad);
					
					// Mensaje de depuracion
					console.log($("#utilidad1").attr('value'));
			});	
			
			// Nota: si hacemos write de "data" que era donde guardabamos lo leido en el fs, no funcionara, ya que cheerio
			// almacena los datos internamente, no hace cambios sobre data. Para ello hacemos write de todo el documento,
			// que se hace en Jquery con $.html()
			res.write($.html());
			
			// End del mensaje, si no, el navegador sigue esperando una respuesta
			res.end();
		}
		});
	}
	else{
		// Para el resto de urls comprobamos si hay parametros, esto funciona solo con GET, para otro metodo habria que modificarlo
		queryObject = url.parse(req.url,true).query;
		console.log(queryObject);		

		// Para obtener el valor pasado por GET simplemente hacemos queryObject["parametro"]
		// Cuidado que se devuelve como String, no como int por lo que tenemos que convertirlo
		let id = parseInt(sanitize(queryObject["id"]));
		let ut = parseInt(sanitize(queryObject["utilidad"]));
		let ca = parseInt(sanitize(queryObject["calidad"]));
		
		// mensaje de depuracion
		console.log("id :"+id+" utilidad "+ut+" calidad "+ca);
		
		// Si el seminario existe, lo guardamos
		if (id && ut && ca){
			console.log("Existe seminario "+String(db.get("seminarios").find({ "id": id }).get("id")));
			// Realizar el assign con varios valores no funcionaba, supongo que tiene que ser un valor cada vez que se llama
			db.get("seminarios").find({ "id": id }).assign({ "calidad": ca }).write();
			db.get("seminarios").find({ "id": id }).assign({ "utilidad": ut }).write();

			
		}
	}
	
});  

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
