DOCKER_COMPOSE := docker compose -f ../docker/compose.yml --env-file ../env/.env.$(ENV) --profile
DOCKER_EXEC := docker exec $(APP_NAME)_backend
DOCKER_PROFILE ?= main
MANAGE = poetry run python manage.py

# -------------- DOCKER --------------

# Runs containers
# DOCKER_PROFILE options: main, secondary. Example: make -f Makefile.local run DOCKER_PROFILE=main
.PHONY: run
run:
	$(DOCKER_COMPOSE) $(DOCKER_PROFILE) up -d --build

# Removes containers
# DOCKER_PROFILE options: main, secondary. Example: make -f Makefile.local stop DOCKER_PROFILE=main
.PHONY: stop
stop:
	$(DOCKER_COMPOSE) $(DOCKER_PROFILE) down

# Enters backend container
.PHONY: entercontainer
entercontainer:
	$(DOCKER_EXEC) sh


# -------------- DJANGO --------------

# Creates an app. Example: make startapp DJANGOAPP=album
.PHONY: startapp
startapp:
	$(DOCKER_EXEC) $(MANAGE) startapp $(DJANGOAPP)

# Creates superuser
.PHONY: createsuperuser
createsuperuser:
	$(DOCKER_EXEC) $(MANAGE) createsuperuser --noinput


# -------------- LINTER --------------

# Checks code style
.PHONY: linter
linter:
	$(DOCKER_EXEC) poetry run flake8 --max-line-length 88
