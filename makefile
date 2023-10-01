
build:
	docker compose build

shell_plus:
	docker compose run --rm app python manage.py shell_plus

runserver:
	docker compose run --rm app python server/server.py
	
runns:
	docker compose run --rm app pyro4-ns

runclient:
	docker compose run --rm app python client/client.py
