COMPOSE_FILE := docker/docker-compose.yml

.PHONY: start stop format lint source test test-unit test-integration test-smoke run

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


source:
	. ./.env && . ./dataworks_venv/bin/activate && bash

test:
	python -m pytest --cov=src

test-unit:
	python -m pytest -m unit

test-integration:
	python -m pytest -m integration

test-smoke:
	python -m pytest -m smoke

run:
	python -m src.main