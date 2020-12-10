![yamdb_push_workflow](https://github.com/fromRussiaImportLove/yamdb_final/workflows/yamdb_push_workflow/badge.svg)

# proEda / прое́да


Multi-user service for noting recipes, ingredients and cooking them.
Users can make bookmark recipe and other author, add recipe to basket 
where calculate how much of each ingredient need to buy. 
It's have API for some function, relized by java-script.

## Getting Started

These instructions will get you a copy of the project up and running 
on your local machine for development and testing purposes. 
See deployment for notes on how to deploy the project on a live system.
For fast start or try project and full base with recipes, you can use
scipt, which download data about dishes and pull picture them from wikipedia.

### Prerequisites

What things you need to install the software and how to install them

```
[https://docker.com](docker 19.03)
[https://docs.docker.com/compose/install/](docker-compose 1.25.0)
[https://python.org](python 3.8+)
```

### Installing

For install you need clone repository, configure .env for settings, 
build docker containers, run services, make migrations, 
and if need make new superuser, prepare data from wikipedia and load fixtures.

You can just start my bash-script ./install.sh

or make these commands:

```
git clone https://github.com/fromRussiaImportLove/foodgram.git
cd foodgram
mv .env-exampe .env
vim .env # for making environment
docker-compose -d up
docker-compose run web python manage.py migrate
docker-compose run web python manage.py loaddata fixtures.json
```

If your need create new superuser
```
docker-compose run web python manage.py createsuperuser
```

For check correct installation, open in browser link: http://127.0.0.1:8000/

## Security Note

For security reason you have edit .env file before build image. 


## Built With

* Django 3.0 [https://www.djangoproject.com/]
* Django-REST-Framework 3.11 [django-rest-framework.org]

## Contributing

If you want contribute, do it. 

## Author

Patsy Charmer. My git (there)[https://github.com/fromRussiaImportLove]
 