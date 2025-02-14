from .models import Vulnerabilidad, Deteccion, DeteccionExp,  Expresion, RequiereExpresion
import re
import json
from .html_parser import MyHTMLParser
from django.core.files import File


# Funcion que obtiene los posibles candidatos en funcion a un tipo de expresion de esprima
#	tipo: tipo de expresion, ej "VariableDeclarator"
#	analisis: analisis lexico de un archivo js
#
#	return: todas las apariciones del tipo dado en el analisis

def BuscaCandidatos(tipo, analisis):
	
	if isinstance(analisis, dict):
		if "type" in analisis.keys():
			if analisis["type"] == tipo:
				encontrado = analisis
				yield encontrado
		for k,v in analisis.items():
			if isinstance(v, (dict,list)):
				yield from BuscaCandidatos(tipo, v)
	elif isinstance(analisis, list):
		for item in analisis:
			if isinstance(item, (dict,list)):
				yield from BuscaCandidatos(tipo, item)
	
# Funcion que comprueba si dos expresiones en json son iguales, funcion recursiva
#	candidato: expresion obtenida del analisis
#	exp: json perteneciente a una expresion
#	variables: conjunto de variables a comparar
#
#	return: lista de variables(False en la casilla que no coincida)

def CompruebaParecido(candidato, exp, variables=[]):

	if isinstance(candidato, dict) and isinstance(exp, dict):

		for (k,v) in exp.items():
			if isinstance(v, (dict,list)) and k in candidato.keys():

				yield from CompruebaParecido(candidato[k],v, variables)	
			elif k in candidato.keys():
				
				if str(v) == "variable":
					yield str(candidato[k])
				elif str(v) == "usa_variable":
				
					if candidato[k] in variables:
						yield str(candidato[k])	
					else:
						yield "False"
				elif "contiene" in v:
					elemento = v.replace("contiene:", "")
					if str(elemento) in str(candidato[k]):
						yield candidato[k]
					else:
						yield "No contiene: "+str(candidato[k])
						yield "False"	
				elif str(v) != str(candidato[k]) and str(v) != "ignora":

					yield "False"	
				
				elif str(v) == str(candidato[k]):
					yield "Ok"
			elif k not in candidato.keys():

				yield "False"
	elif isinstance(candidato, list) and isinstance(exp, list):

		for c,e in zip(candidato,exp):
			yield from CompruebaParecido(c, e, variables)
	else: 

		yield "False"	
	
# Funcion que comprueba si un candidato contiene una expresion html
#	candidato: expresion obtenida del analisis
#	exp: json de un objeto expresion para codigo html
#
#	return: lista de variables(False en la casilla que no coincida)

def CompruebaContiene(candidato, exp):
	if len(candidato) < len(exp):
		yield "False"
	elif isinstance(candidato, dict) and isinstance(exp, dict):
		for (k,v)in exp.items():
			if k in candidato.keys():
				if isinstance(v, (dict,list)):
					yield from CompruebaContiene(candidato[k], v)
				elif "contiene" in v:
					elemento = v.replace("contiene:", "")
					if str(elemento) in str(candidato[k]):
						yield candidato[k]
					else:
						yield "No contiene: "+str(candidato[k])
						yield "False"
				else:
					if "contiene" not in v and v != candidato[k]:
						yield "False"
			else:
				yield "False"	

	elif isinstance(candidato, list) and isinstance(exp, list):
		for e in exp:
			k = e.keys()
			for c in candidato:
				check =  any(item in k for item in c.keys())
				if check:
					existe_key = True
					yield from CompruebaContiene(c, e)
				
	else: 
		if "contiene" in exp:
			elemento = exp.replace("contiene:", "")
			if elemento in candidato:
				yield candidato
			else:
				yield "False"
		elif exp != candidato:
			yield "False"	



# Funcion que comprueba si una expresion json existe en el analisis lexico diferenciando html y js
#	exp: objeto expresion
#	analisis_lexico: analisis lexico de un archivo
#	variables: conjunto de variables a comparar
#
#	return: lista de variables(False en caso de no coincidir) o True/False

def ContieneExpresion(exp, analisis_lexico, variables=[]):
	contiene_expresion = False
	variables_encontradas = []
	print("COMPROBANDO EXPRESION: "+str(exp.nombre_expresion)+" con las variables"+str(variables))
	if "type" in exp.json.keys():
		tipo = exp.json["type"]
		print("Inicio de candidatos")
		candidatos = list(BuscaCandidatos(tipo, analisis_lexico))	
		
		for c in candidatos:

			parecido = CompruebaParecido(c, exp.json, variables)
			print("Candidato tipo: "+str(type(c))+ " valor: "+str(c))
			encontrado = True
			for p in parecido:
	
				print(str(p))
				if p == "False":
					encontrado = False
				else:
					variables_encontradas.append(p)		
			if encontrado:
				print("No he encontrado FALSE")
				contiene_expresion = True
				if exp.tipo == "variable" or exp.tipo == "uso_de_variable":
					print("variables encontradas: "+str(variables_encontradas))
					contiene_expresion = variables_encontradas
			elif not encontrado:
				variables_encontradas = []
				
	if "encuentra" in exp.json.keys():
		print("BUSCANDO: --> " +str(exp.json["encuentra"]))
		tipo = exp.json["encuentra"]["tipo"]
		print("TIPO: "+str(tipo))
		expresion = exp.json["encuentra"]["contiene"]
		print("EXPRESION: "+str(expresion))
		candidatos = list(BuscaCandidatos(tipo, analisis_lexico))	
		for c in candidatos:
			encontrado = True
			print("Candidato tipo: "+str(type(c))+ " valor: "+str(c))
			parecido = CompruebaContiene(c, expresion)
			for p in parecido:
				print(p)
				if p == "False":
					encontrado = False
				else:
					variables_encontradas.append(p)		
			if encontrado:
				print("No he encontrado FALSE")
				contiene_expresion = True
				if exp.tipo == "variable" or exp.tipo == "uso_de_variable":
					contiene_expresion = variables_encontradas
			elif not encontrado:
				variables_encontradas = []
	print("paso: "+str(contiene_expresion))
	return contiene_expresion



# Funcion que añade las detecciones a la base de datos y devuelve el tipo de mensaje(warning, danger,...)
#	expresion: objeto expresion
#	analisis: objeto analisis
#
#	return: dict con el nombre y la descripcion de la expresion

def DetectadaExpresion(expresion, analisis):

	vulnerabilidad = expresion.vulnerabilidad

	nueva_deteccion = Deteccion(titulo_analisis=analisis, vulnerabilidad=vulnerabilidad)
	nueva_deteccion.save()

	nueva_deteccion_exp = DeteccionExp(titulo_analisis=analisis, expresion=expresion)
	nueva_deteccion_exp.save()

	return {"nombre": expresion.nombre_expresion, "descripcion": expresion.descripcion}


# Funcion que comprueba si una expresion y sus requisitos estan contenidos en un analisis dado
#	analisis_lexico: analisis lexico de un archivo en formato dict
#	expresion: objeto expresion a comprobar
#	variables: conjunto de variables a comparar
#
#	return: lista de expresiones con las detecciones encontradas

def CompruebaExpresion(analisis_lexico, expresion, variables=[]):
	expresiones = []

	#print("variables para expresion: "+str(expresion.nombre_expresion)+" variables: "+str(variables))
	contiene = ContieneExpresion(expresion, analisis_lexico, variables)
	#print("Contiene Expresion: "+str(contiene))
	if (contiene and not expresion.incluido_o_excluido) or (not contiene and expresion.incluido_o_excluido):

		expresiones.append(expresion.id_expresion)
		print("Contiene expresion: "+str(expresion.nombre_expresion))
		if expresion.tipo == "variable" or expresion.tipo == "uso_de_variable":

			for c in contiene:
				if c != "Ok":
					variables.append(c)
			print("Tratamos busqueda de variables: "+str(variables))
		requisitos = RequiereExpresion.objects.filter(expresion_primaria=expresion)
		if requisitos:

			for req in requisitos:
				print("Comprobando requisito: "+str(req.expresion_requerida))
				contiene_requisito = CompruebaExpresion(analisis_lexico, req.expresion_requerida, variables)
				print("Contiene: "+str(contiene_requisito))
				if (contiene_requisito and not req.expresion_requerida.incluido_o_excluido) or (not contiene_requisito and req.expresion_requerida.incluido_o_excluido):

					for r in contiene_requisito:
						expresiones.append(r)

	return expresiones

# Funcion que comprueba si un analisis dado contiene una vulnerabilidad indicada
#	analisis_lexico: analisis lexico de un archivo
#	vulnerabilidad: objeto vulnerabilidad para comprobar
#
#	return: lista con las expresiones asociadas a la vulnerabilidad encontradas

def CompruebaVulnerabilidad(analisis_lexico, vulnerabilidad):
	variables = []
	detecciones = []

		
	expresiones = Expresion.objects.filter(vulnerabilidad=vulnerabilidad, primera=True)
	for exp in expresiones:

		print("Comprobando expresion: "+str(exp.nombre_expresion))
		detectado = CompruebaExpresion(analisis_lexico, exp, variables)
		if detectado:

			print("Expresion detectada")
			for d in detectado:

				detecciones.append(d)

	return detecciones


