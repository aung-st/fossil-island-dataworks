COMPOSE_FILE := docker/docker-compose.yml

.PHONY: start stop format lint

start:
	docker compose -f $(COMPOSE_FILE) up -d

stop:
	docker compose -f $(COMPOSE_FILE) down

format:
	ruff format .

lint:
	ruff check .

fix: 
	ruff format . 
	ruff check . --fix
	
