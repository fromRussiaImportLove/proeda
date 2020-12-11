#!/bin/bash

# git clone https://github.com/fromRussiaImportLove/foodgram_project.git
# cd foodgram_project
cp .env-example .env
vim .env
docker-compose -d up
docker-compose run web python manage.py migrate
docker-compose run web python manage.py generate_test_users
docker-compose run web python manage.py generate_ingredients
docker-compose run web python manage.py fetch_dishes_from_wiki
docker-compose run web python manage.py generatate_dishes

