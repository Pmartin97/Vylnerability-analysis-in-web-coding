
all:
	docker-compose up

build:
	docker-compose build

django-startproject:
	sudo docker-compose run web django-admin startproject sitio_web .
	sudo chown -R ${USER}:${USER} .

django-startapp:
	sudo docker-compose run web python manage.py startapp grd
	sudo chown -R ${USER}:${USER} .

django-migrate:
	sudo docker-compose run web python3 manage.py migrate

django-createsuperuser:
	sudo docker-compose run web python3 manage.py createsuperuser
