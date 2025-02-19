DOCKER_COMPOSE := docker compose -f ../docker/compose.yml --env-file ../env/.env.$(ENV) --profile
DOCKER_EXEC := docker exec $(APP_NAME)_backend
DOCKER_PROFILE ?= main
MANAGE = poetry run python manage.py

# -------------- DOCKER --------------

# Runs containers
# DOCKER_PROFILE options: main, secondary. Example: make run DOCKER_PROFILE=main
.PHONY: run
run:
	$(DOCKER_COMPOSE) $(DOCKER_PROFILE) up -d --build

# Removes containers
# DOCKER_PROFILE options: main, secondary. Example: make stop DOCKER_PROFILE=main
.PHONY: stop
stop:
	$(DOCKER_COMPOSE) $(DOCKER_PROFILE) down

# Enters backend container
.PHONY: entercontainer
entercontainer:
	$(DOCKER_EXEC) sh
