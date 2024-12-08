p-build:
	docker compose -f ./docker-compose.yml up --build -d 

p-down:
	docker compose -f ./docker-compose.yml  down


p-logs:
	docker compose -f ./docker-compose.yml logs


shell:
	docker exec -it web bash

superuser:
	docker exec -it web python manage.py createsuperuser