.PHONY: up down logs rebuild

up:
	docker compose -f compose.observability.yml up -d
	docker compose -f compose.apps.yml up -d --build

down:

	docker compose -f compose.observability.yml down
	docker compose -f compose.apps.yml down

rebuild:
	docker compose -f compose.apps.yml down
	docker compose -f compose.observability.yml down
	docker compose -f compose.observability.yml up -d
	docker compose -f compose.apps.yml up -d --build

logs:
	docker compose -f compose.apps.yml logs -f
