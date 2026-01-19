.PHONY: up down logs rebuild

up:
	docker compose -f compose.observability.yml up -d
	docker compose -f compose.apps.yml up -d --build

down:

	docker compose -f compose.observability.yml down -v
	docker compose -f compose.apps.yml down -v

rebuild:
	docker compose -f compose.apps.yml down -v
	docker compose -f compose.observability.yml down -v
	docker compose -f compose.observability.yml up -d
	docker compose -f compose.apps.yml up -d --build

logs:
	docker compose -f compose.apps.yml logs -f
