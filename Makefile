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

alembic-generate:
	poetry run alembic revision --autogenerate

alembic-migrate:
	poetry run alembic upgrade head

build-run-application: build-application run-application

build-run-application-test: build-application-test run-application-test

build-application-test:
	docker compose -f docker-compose.test.yml build --no-cache

run-application-test-decouple:
	docker compose -f docker-compose.test.yml up -d

get-application-test-logs:
	docker logs application-test -f

run-application-test: run-application-test-decouple get-application-test-logs stop-containers
