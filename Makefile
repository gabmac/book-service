# Get the list of volume names
VOLUMES := $(shell docker volume ls -q)

# Get the list of container names
CONTAINERS := $(shell docker ps -qa)

# Stop all containers
stop-containers:
	docker stop $(CONTAINERS)

# Task to list volume names
list-volumes-names:
	@echo $(VOLUMES)

clean-containers:
	docker system prune -f

clean-containers: stop-containers clean-containers

# Task to remove all volumes
remove-volumes:
	docker volume prune -f
	docker volume rm -f $(VOLUMES)

clean-volumes: clean-containers remove-volumes

build-application:
	docker compose build --no-cache

run-application:
	docker compose up

setup-dev-environment:
	poetry install

alembic-upgrade:
	alembic upgrade head

alembic-migrate:
	poetry run alembic upgrade head

build-run-application: build-application run-application alembic-upgrade
