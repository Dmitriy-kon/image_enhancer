local:
	docker compose -f docker-compose-local.yml up

local-build:
	docker compose -f docker-compose-local.yml up --build

local-down:
	docker compose -f docker-compose-local.yml down

prod:
	docker compose -f docker-compose-prod.yml up

prod-build:
	docker compose -f docker-compose-prod.yml up --build

prod-down:
	docker compose -f docker-compose-prod.yml down