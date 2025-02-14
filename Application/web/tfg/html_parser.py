from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
	def __init__(self):
		super().__init__(convert_charrefs=False)
		self.reset()
		self.script = False
		self.inputs = 0
		self.datos = []
		self.form = []
		self.elementos = []
	
	def handle_starttag(self, tag, attrs):
		tipo = "none"
		nombre = "none"
		elemento = []
		for attr in attrs:
			elemento.append( {attr[0]: attr[1]})
			if attr[0] == "type":
				tipo = attr[1]
			if attr[0] == "name":
				nombre = attr[1]
		self.elementos.append({ "type": tag, "attrs": elemento })
		if tag == "script":
			self.script = True
			
		elif tag == "input" and tipo != "submit":
			self.form.append({ "input": tipo, "nombre": nombre, "attrs": attrs})
			self.inputs += 1
		else:
			self.script = False


	def handle_endtag(self, tag):
		self.script = False


	def handle_data(self, data):
		if self.script == True:
			data = data.replace('\t', ' ')
			data = data.replace(u'\xa0', ' ')
			data = data.replace('\n', ' ')
			self.datos.append(data)

	def get_elementos(self):
		return self.elementos

	def get_datos(self):
		return ''.join(self.datos)
	def get_inputs(self):
		result = []
		for i in self.form:
			result.append(i)
		return result

