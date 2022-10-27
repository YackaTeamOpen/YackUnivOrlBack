
# Classic install process of the venv with dependencies

dev-install-apt:
	bash scripts/install-apt.sh

dev-install-venv: dev-clean-venv dev-install-apt
	bash scripts/install-venv.sh
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r install/reqs.txt

dev-clean-venv:
	rm -rf .venv

# Classic db setup is 
# make dev-setup-db // first time only or to reset
# make dev-populate-db

dev-setup-db:
	bash scripts/update-db.sh

dev-populate-db:
	bash scripts/populate-db.sh

dev-yacka-user-init:
	bash scripts/init-yacka-user.sh

run-dev:
	export FLASK_APP=app/pywsgi.py; \
	export FLASK_ENV=local; \
	flask run

run:
	export FLASK_APP=app/pywsgi.py; \
	export FLASK_ENV=production; \
	flask run

build-and-run-alpha:
	bash install/build-and-run-image.sh yackapi-alpha

init-alpha-db:
	export FLASK_APP=app/yacka.py; \
	export INIT_CONT_NAME=cnt-a-yackapi; \
	export INIT_CONT_DBNAME=cnt-a-yackapi-sql; \
	export INIT_DB_PORT=3307; \
	export DB_NAME=yackadb; \
	export DB_ADMIN=admin_yacka; \
	export DB_ADMIN_PASS=YPcpLfL3z7FXLT; \
	export DB_INIT_FILE=yacka_develop; \
	bash install/init-docker-db.sh
	
populate-alpha-db:
	export FLASK_APP=app/yacka.py; \
	export INIT_CONT_NAME=cnt-a-yackapi; \
	bash install/populate-docker-db.sh

alpha-yacka-user-init:
	export FLASK_APP=app/yacka.py; \
	export INIT_CONT_NAME=cnt-a-yackapi; \
	bash install/init-yacka-user.sh

stop-alpha:
	bash install/stop-image.sh yackapi-alpha

build-and-run-prod:
	bash install/build-and-run-image.sh yackapi-prod
	
init-prod-db:
	export FLASK_APP=app/yacka.py; \
	export INIT_CONT_NAME=cnt-p-yackapi; \
	export INIT_CONT_DBNAME=cnt-p-yackapi-sql; \
	export INIT_DB_PORT=3306; \
	export DB_NAME=yackadb; \
	export DB_ADMIN=admin_yacka; \
	export DB_ADMIN_PASS=YPcpLfL3z7FXLT; \
	export DB_INIT_FILE=yacka_develop; \
	bash install/init-docker-db.sh

populate-prod-db:
	export FLASK_APP=app/yacka.py; \
	export INIT_CONT_NAME=cnt-p-yackapi; \
	bash install/populate-docker-db.sh

prod-yacka-user-init:
	export FLASK_APP=app/yacka.py; \
	export INIT_CONT_NAME=cnt-p-yackapi; \
	bash install/init-yacka-user.sh

stop-prod:
	bash install/stop-image.sh yackapi-prod

git-pull:
	git pull

upgrade-alpha:
	bash install/build-and-release.sh alpha

upgrade-production:
	bash install/build-and-release.sh production

migrate-db-alpha:
	bash install/migrate-db.sh alpha

migrate-db-production:
	bash install/migrate-db.sh production