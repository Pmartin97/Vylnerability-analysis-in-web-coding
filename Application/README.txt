
Instalacion y puesta en marcha de la aplicacion:
	sudo make

Creacion de usuario administrador
	sudo make django-createsuperuser

Direcciones del sitio:

Aplicacion: 	localhost:8000/accounst/login
Administracion:   localhost:8000/admin

Requisitos:
	docker-compose
	python 2.7 min*

Nota:
* En caso de ejecutarse fuera del entorno de docker.

En caso de no realizar build la primera vez que se ejecute el makefile,
se puede hacer mediante el comando "sudo make build".
Los templates utilizan cdn, se puede obviar la carpeta static.

Archivos:

	configuracion de django:
		/Dai/web/sitio_web/

	urls, models, formularios y views de la aplicacion:
		/Dai/web/tfg/[urls.py, models.py, forms.py, views.py]

	templates:
		/Dai/web/templates[/accounts]

	Biblioteca con funciones que utiliza la aplicacion:
		/Dai/web/tfg/lib.py
		/Dai/web/tfg/analyze.py

	Almacenamiento de los archivos de usuarios:
		/Dai/web/files/[user_id, analyze/]

