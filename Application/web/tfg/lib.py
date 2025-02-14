from .models import Vulnerabilidad, Deteccion, DeteccionExp, Expresion, RequiereExpresion
from .html_parser import MyHTMLParser
import esprima
import json
import math
import datetime
from django.utils import timezone
import re
from .analyze import CompruebaVulnerabilidad, DetectadaExpresion


def insert_str(string, str_to_insert, index):
    return string[:index] + str_to_insert + string[index:]

# Funcion que calcula el top de las 10 vulnerabilidades mas detectadas
def TopVulnerabilidades():
	top = {}
	detecciones = Deteccion.objects.all()
	for d in detecciones:

		if d.vulnerabilidad.cve not in top.keys():
			top[d.vulnerabilidad.cve] = 0
		if d.vulnerabilidad.cve in top.keys():
			top[d.vulnerabilidad.cve] = top[d.vulnerabilidad.cve]+1
	print("top: "+str(top))
	top_d = sorted(top, key=top.get, reverse=True)
	print("top_d: "+str(top_d))
	top_f = top_d[:10]
	
	return top_f

# Funcion que calcula el nº en el top de la vulnerabilidad dada
def TopVulnerabilidad(vulnerabilidad):
	top = {}
	detecciones = Deteccion.objects.all()
	for d in detecciones:
		if not d.vulnerabilidad in top.keys():
			top[d.vulnerabilidad.cve] = 0
		else:
			top[d.vulnerabilidad.cve] += 1
	top_d = sorted(top, key=top.get, reverse=True)
	count = 1
	real_top= "Not match"
	for t in top_d:
		if t == vulnerabilidad.cve:
			real_top = count
		else:
			count += 1
	
	return real_top

# Funcion que calcula las detecciones realizadas del top 10 dado en todo el mes
def DeteccionesMes(top):
	today = timezone.now()
	dias = 30 - today.day
	first = today.replace(day=1)
	lastMonth = first - datetime.timedelta(days=1)
	lastMonth = lastMonth - datetime.timedelta(days=dias)
	print("HOY: "+str(today)+ "- Ultimo mes: "+str(lastMonth))
	det = {}
	for v in top:

		vul = Vulnerabilidad.objects.get(cve=v)
		detecciones = Deteccion.objects.filter(fecha__range=[lastMonth, today], vulnerabilidad=vul)
		for d in detecciones:
			fecha = min(math.ceil(d.fecha.day/7)-1, 3)
			if d.vulnerabilidad.cve in det.keys():
				det[d.vulnerabilidad.cve][fecha] += 1
			else:
				det[d.vulnerabilidad.cve] = [0,0,0,0]
				det[d.vulnerabilidad.cve][fecha] = 1
	return det

# Funcion que calcula el numero de detecciones de la vulnerabilidad dada en todo el mes
def DeteccionesMesVulnerabilidad(vul):
	today = timezone.now()
	dias = 30 - today.day
	first = today.replace(day=1)
	lastMonth = first - datetime.timedelta(days=1)
	lastMonth = lastMonth - datetime.timedelta(days=dias)
	print("HOY: "+str(today)+ "- Ultimo mes: "+str(lastMonth))
	det = {}
	detecciones = Deteccion.objects.filter(fecha__range=[lastMonth, today], vulnerabilidad=vul)
	for d in detecciones:
		fecha = min(math.ceil(d.fecha.day/7)-1, 3)
		if vul.cve in det.keys():
			det[vul.cve][fecha] += 1
		else:
			det[vul.cve] = [0,0,0,0]
			det[vul.cve][fecha] = 1
	
	return det

# Funcion que calcula el numero de detecciones de las expresiones asociadas a una vulnerabilidad en todo el mes
def DeteccionesExpMesVulnerabilidad(vul):
	today = timezone.now()
	dias = 30 - today.day
	first = today.replace(day=1)
	lastMonth = first - datetime.timedelta(days=1)
	lastMonth = lastMonth - datetime.timedelta(days=dias)
	print("HOY: "+str(today)+ "- Ultimo mes: "+str(lastMonth))

	expresiones = {}
	
	exp = Expresion.objects.filter(vulnerabilidad=vul)
	for e in exp:
		#print("expresion: "+str(e))
		detecciones = DeteccionExp.objects.filter(fecha__range=[lastMonth, today], expresion=e)
		for d in detecciones:
			fecha = min(math.ceil(d.fecha.day/7)-1, 3)
			if d.expresion.nombre_expresion in expresiones.keys():
				if expresiones[d.expresion.nombre_expresion][fecha]:
					expresiones[d.expresion.nombre_expresion][fecha] += 1
			if not d.expresion.nombre_expresion in expresiones.keys():
				expresiones[d.expresion.nombre_expresion] = [0,0,0,0]
				expresiones[d.expresion.nombre_expresion][fecha] = 1		
	return expresiones


# Funcion que realzia el analisis sintactico de un documento
def AnalisisSintactico(documento):
	tokens = esprima.tokenize(documento)
	return tokens


# Funcion que realiza el analisis lexico de un documento
def AnalisisLexico(codigo, rango=False):
	analisis = esprima.parseScript(codigo, { 'tokens': True, 'range': rango, 'tolerant': True})
	return analisis



# Funcion que comprueba las vulnerabilidades basadas en acciones:
#	analisis_lexico: analisis del documento
#	archivo: objeto archivo
#	tipo_archivo: framework de trabajo del archivo
#	analisis: objeto analisis resultado
#
#	return lista con las vulnerabilidades encontradas

def Analiza_acciones(analisis_lexico, archivo, tipo_archivo, analisis):
	
	resultados = []
	
	if tipo_archivo == "unknown":

		vulnerabilidades = Vulnerabilidad.objects.filter(clase_vulnerabilidad='acciones')
	else:

		vulnerabilidades = Vulnerabilidad.objects.filter(clase_vulnerabilidad='acciones', framework=tipo_archivo)
		unknown = Vulnerabilidad.objects.filter(clase_vulnerabilidad="acciones", framework="unknown")
		for v in unknown:
			detecciones = []
			deteccion = CompruebaVulnerabilidad(analisis_lexico, v)
			if deteccion:

				ultima = False
				print("detectado: "+str(deteccion))
				for d in deteccion:
					print("DETECCION: "+str(d))
					exp = Expresion.objects.get(id_expresion=d)
					if exp.ultima == True:
						ultima = True				
				if ultima:

					for d in deteccion:
						exp = Expresion.objects.get(id_expresion=d)				
						datos = DetectadaExpresion(exp, analisis)
						detecciones.append(datos)
					resultados.append({"vulnerabilidad": v.cve, "expresiones": detecciones})
	
	for v in vulnerabilidades:

		detecciones = []
		deteccion = CompruebaVulnerabilidad(analisis_lexico, v)
		if deteccion:

			ultima = False
			print("detectado: "+str(deteccion))
			for d in deteccion:
				print("DETECCION: "+str(d))
				exp = Expresion.objects.get(id_expresion=d)
				if exp.ultima == True:
					ultima = True				
			if ultima:

				for d in deteccion:
					exp = Expresion.objects.get(id_expresion=d)				
					datos = DetectadaExpresion(exp, analisis)
					detecciones.append(datos)
				resultados.append({"vulnerabilidad": v.cve, "expresiones": detecciones})

	return { "vulnerabilidades": resultados}


# Funcion que comprueba las vulnerabilidades basadas en terceros:
#	analisis_lexico: analisis del documento
#	archivo: objeto archivo
#	tipo_archivo: framework de trabajo del archivo
#	analisis: objeto analisis resultado
#
#	return lista con las vulnerabilidades encontradas
def Analiza_terceros(analisis_lexico, archivo, tipo_archivo, analisis):
	
	resultados = []

	if tipo_archivo == "unknown":

		vulnerabilidades = Vulnerabilidad.objects.filter(clase_vulnerabilidad='terceros')
	else:

		vulnerabilidades = Vulnerabilidad.objects.filter(clase_vulnerabilidad='terceros', framework=tipo_archivo)	
	
	for v in vulnerabilidades:
		detecciones = []		
		deteccion = CompruebaVulnerabilidad(analisis_lexico, v)
		if deteccion:

			ultima = False
			print("detectado: "+str(deteccion))
			for d in deteccion:
				print("DETECCION: "+str(d))
				exp = Expresion.objects.get(id_expresion=d)
				if exp.ultima == True:
					ultima = True				
			if ultima:
				for d in deteccion:
					exp = Expresion.objects.get(id_expresion=d)				
					datos = DetectadaExpresion(exp, analisis)
					detecciones.append(datos)
				resultados.append({"vulnerabilidad": v.cve, "expresiones": detecciones})

	return {"vulnerabilidades": resultados}


# Funcion que realiza el analisis de un archivo y devuelve la lista completa de vulnerabilidades
#	archivo: objeto archivo a analizar
#	analisis: objeto analisis resultado
#
#	return: lista completa de vulnerabilidades de acciones y terceros

def Analiza(archivo, analisis):

	with open (archivo.archivo.path, "r") as myfile:
		data=myfile.read()

	#Comprobamos tipo de archivo, html, solo js, nodejs,...

	tipo_archivo = archivo.framework
	if tipo_archivo == "html":
		parser = MyHTMLParser()
		parser.feed(data)
		codigo = parser.get_datos()
	else:
		codigo = data

	# Realizamos el analisis lexico
	if len(codigo) != 0:
		analisis_lexico = AnalisisLexico(codigo, False).toDict()
		if tipo_archivo == "html":
			elementos = parser.get_elementos()
			analisis_lexico["elementos"] = elementos
		print("Analizamos el codigo")
		# Realizamos comprobacion de vulnerabilidades con el analisis
		detecciones_terceros = Analiza_terceros(analisis_lexico, codigo, tipo_archivo, analisis)
		detecciones_acciones = Analiza_acciones(analisis_lexico, codigo,  tipo_archivo, analisis)

	#Append las detecciones de uno al otro y return
		print("terceros: ")
		print(str(detecciones_terceros))
		print("acciones: ")
		print(str(detecciones_acciones))
		return { "terceros": detecciones_terceros, "acciones": detecciones_acciones}
	else:
		return {}

# Funcion que genera el codigo html necesario para el documento analisis
#	nombre: nombre del archivo analizado
#	vulnerabilidades: lista de vulnerabilidades completas
#	codigo: codigo fuente del archivo analizado
#
#	return: pagina html en formato string

def CreaHTML( nombre, vulnerabilidades, codigo):
	print(str(vulnerabilidades))
	terceros = {}
	acciones = {}
	if "terceros" in vulnerabilidades:
		terceros = vulnerabilidades["terceros"]
	if "acciones" in vulnerabilidades:
		acciones = vulnerabilidades["acciones"]
	pagina = "<!doctype html><html><head><title>"+nombre+"</title>"
	
	pagina = pagina + "</head><body><h3>"+nombre+" analyzed </h3>"
	pagina = pagina + "<section><h2><b>Vulnerabilities found</b></h2><div class='panel-group'>"

	if('vulnerabilidades' in terceros):
		for t in terceros["vulnerabilidades"]:
			ide = t["vulnerabilidad"]
			vuln = Vulnerabilidad.objects.get(cve=ide)			

			pagina = pagina + "<div class='panel panel-warning '>"
			pagina = pagina + "<div class='panel panel-heading bg-warning text-dark' role='button'  id='toggle"+ide+"' data-toggle='collapse' href='#"+ide+"' >"
			pagina = pagina + ide
			pagina = pagina + "</div>"
			pagina = pagina + "<div	id='"+ide+"' class='panel-collapse panel-body collapse' >"		
			pagina = pagina + "Score: "+str(vuln.base_score)+"<br> Description: "+vuln.description
			pagina = pagina + ""

			expresiones = t["expresiones"]
			for e in expresiones:
				nombre = e["nombre"].replace(" ", "_")
				descripcion = e["descripcion"]
				ide = str(ide)+nombre
				pagina = pagina + "<div class='panel panel-danger '>"
				pagina = pagina + "<div class='panel panel-heading bg-danger text-white' role='button'  id='toggle"+ide+"' data-toggle='collapse' href='#"+ide+"' >"
				pagina = pagina + nombre
				pagina = pagina + "</div>"
				pagina = pagina + "<div	id='"+ide+"' class='panel-collapse panel-body collapse' >"		
				pagina = pagina + "<br> Description: "+descripcion
				pagina = pagina + "</div></div>"
			pagina = pagina + "</div></div>"
	if('vulnerabilidades' in acciones):
		for t in acciones["vulnerabilidades"]:
			ide = t["vulnerabilidad"]
			vuln = Vulnerabilidad.objects.get(cve=ide)
			pagina = pagina + "<div class='panel panel-info '>"
			pagina = pagina + "<div class='panel panel-heading ' role='button'  id='toggle"+ide+"' data-toggle='collapse' href='#"+ide+"' >"
			pagina = pagina + ide
			pagina = pagina + "</div>"
			pagina = pagina + "<div	id='"+ide+"' class='panel-collapse panel-body collapse' >"+vuln.description	
			expresiones = t["expresiones"]
			for e in expresiones:
				nombre = e["nombre"].replace(" ", "_")
				descripcion = e["descripcion"]
				pagina = pagina + "<div class='panel panel-info '>"
				pagina = pagina + "<div class='panel panel-heading' role='button'  id='deteccion"+nombre+"' data-toggle='collapse' href='#"+nombre+"' >"
				pagina = pagina + nombre
				pagina = pagina + "</div>"
				pagina = pagina + "<div	id='"+nombre+"' class='panel-collapse panel-body collapse' >"
				pagina = pagina + descripcion	
				pagina = pagina + "</div></div>"


			pagina = pagina + "</div></div>"
	pagina = pagina + "</div></section>"

	pagina = pagina + "<section><h2><b>Code:</b></h2><br><xmp> "+codigo+"</xmp></section></body></html>"
	
	return pagina

# Funcion que devuelve el historial completo de un archivo
def History( query ):
	
	historial = []
	for q in query:
		print("Version id: "+str(q.revision.id))
		historial.append({"version": str(q.revision.date_created), "comentario": q.revision.comment});
	return historial



