# Default target - shows help information
.DEFAULT_GOAL := help

help:  ## Show this help message
	@echo "Available commands:"
	@echo ""
	@echo "Environment Setup:"
	@echo "  setup-dev-environment    Install poetry dependencies for development"
	@echo ""
	@echo "Database Migration:"
	@echo "  alembic-generate         Generate new migration from model changes"
	@echo "  alembic-migrate          Run pending migrations"
	@echo ""
	@echo "Application Management:"
	@echo "  build-application        Build Docker containers without cache"
	@echo "  run-application          Start the application with docker-compose"
	@echo "  build-run-application    Build and run the application"
	@echo ""
	@echo "Testing:"
	@echo "  build-application-test     Build test environment containers"
	@echo "  run-application-test       Run tests in detached mode and show logs"
	@echo "  run-application-test-decouple  Run test containers in background"
	@echo "  get-application-test-logs  Show test application logs"
	@echo "  build-run-application-test Build and run test environment"
	@echo ""
	@echo "Cleanup:"
	@echo "  stop-containers          Stop all running Docker containers"
	@echo "  clean-containers         Remove stopped containers and prune system"
	@echo "  list-volumes-names       List all Docker volume names"
	@echo "  remove-volumes           Remove all Docker volumes"
	@echo "  clean-volumes            Clean containers and remove all volumes"
	@echo ""
	@echo "Usage: make <command>"

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

build-application-test:
	docker compose -f docker-compose.test.yml build --no-cache

run-application-test-decouple:
	docker compose -f docker-compose.test.yml up -d

build-run-application-test: build-application-test run-application-test

get-application-test-logs:
	docker logs application-test -f

run-application-test: run-application-test-decouple get-application-test-logs
