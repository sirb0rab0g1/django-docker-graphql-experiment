docker-compose = docker-compose run api python manage.py

help: # This help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

local: ## Starts the api container for local development
	@echo "\033[92mStarting api container for local development...\033[0m"
	docker-compose up --build api

backend: ## Start the api and nginx container
	@echo "\033[92mStarting an environment for local development...\033[0m"
	docker-compose up --build nginx

migrations: # ex. make migrations name=name_to_commit
	@echo "\033[92mMaking Migrations with a name of $(name) ...\033[0m"
	$(docker-compose) makemigrations

migrate:
	@echo "\033[92mStart Migrating...\033[0m"
	$(docker-compose) migrate
	make local

superuser:
	@echo "\033[92mCreating Super User...\033[0m"
	$(docker-compose) createsuperuser

resetmigration:
	make migrations
	make showmigrations

test-queries:
	${docker-compose} shell < makequeries/queries.py

fakeapp: #example make fakeapp application=request
	@echo "Before using this command i rather make resetmigration first to show which application will be faked"
	@echo "Choose application you want to reset"
ifeq ($(application),)
	echo "Can't Proceed Without putting any values in test"
else
	$(docker-compose) migrate --fake $(application) zero
	find . -path "*/${application}/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/${application}/migrations/*.pyc" -delete
	make showmigrations
	make migrations
	$(docker-compose) migrate --fake-initial # after do `make local` to safety rebuild the application then `make lan`
endif

forcefake: #make forcefake application=<your_app>
	$(docker-compose) migrate --fake $(application)

showmigrations:
	@echo "\033[92mCreating Super User...\033[0m"
	$(docker-compose) showmigrations

editor:
	@echo "\033[92mOpening bpython editor...\033[0m"
	$(docker-compose) shell -i bpython

install: #ex. make install name=name_of_package
	@echo "\033[92mInstalling Pakcage $(name)...\033[0m"
	pipenv install $(name)

uninstall:
	@echo "\033[92mUninstalling Pakcage $(name)...\033[0m"
	pipenv uninstall $(name)

build:
	@echo "\033[92mUninstalling Pakcage $(name)...\033[0m"
	docker-compose build

up:
	@echo "\033[92mRecreating for local development...\033[0m"
	docker-compose up

up-silent:
	docker-compose up -d

down:  ## Down docker containers
	@echo "\033[92mDestroying for local development...\033[0m"
	docker-compose down ${args}

start:
	@echo "\033[92mStarting for local development...\033[0m"
	docker-compose start

stop:
	@echo "\033[92mStopping for local development...\033[0m"
	docker-compose stop

bash:
	docker-compose run api bash

dump:
	# docker-compose exec -u <your_postgres_user> <postgres_service_name> pg_dump -Fc <database_name_here> > db.dump
	docker-compose exec --user postgres db pg_dump -Fp postgres > db.sql

restore:
	cat db.sql | docker exec -i aeon_towers_postgresql psql -U postgres

fix: # this command after installing certain 3rd party
	pip install pipenv
	pipenv run pip install pip==18.0
	pipenv install

fix-lock: # this command will fix package dependencies
	pipenv lock --pre --clear

heroku-login:
	heroku login

heroku-container-login:
	heroku container:login

heroku-container-push:
	heroku container:push web

heroku-container-release:
	heroku container:release web

collect-static:
	$(docker-compose) collectstatic --no-input

rebuild:
	# NOTE steps to rebuild the ssr docker container (will data already)
  # NOTE: if mag push ka ug no existing data i uncomment ang sulod sa entrypoint.sh
	# 1. docker system prune -a --volumes (erase all data)
	# 2. make build (rebuild the machine)
	# 3. make up (install all prerequisites)
	# 4. make down (to shutdown the machine)
	# 4. docker-compose up -d db (to start only the database)
	# 5. make restore (restore the sql file)
	# 6. make down (to shutdown again the again. to refresh the process)
	# 7. make up (to start all containers)

remove-media-file:
# make dump
# push to bitbucket
# make down
# rm -rf media (to remove files)
# mkdir media
# make collect-static
# make build
# make up

rebuild-fresh: # for fresh migration without db
	docker system prune -a --volumes # (erase all data)
	make build
	make up

#clean:
#	docker rmi -f $(docker images | grep "<none>" | awk "{print \$3}")


#reset-db:
#	docker rm $(docker ps -a -q) -f
# docker volume prune

#start new app
# https://docs.djangoproject.com/en/3.0/intro/tutorial01/#creating-the-polls-app
