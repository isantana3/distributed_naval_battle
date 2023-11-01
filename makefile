build:
	docker compose build

shell_plus:
	docker compose run --rm app python manage.py shell_plus

runserver:
	docker compose run --rm app python server/server.py
	
runns:
	docker compose run --rm app pyro4-ns

runclient1:
	docker compose run --rm app python client/client.py 1

runclient2:
	docker compose run --rm app python client/client.py 2

runtestserver:
	docker compose run --rm app python server/test_server.py

runtestclient1:
	docker compose run --rm app python client/test_client.py 1

runtestclient2:
	docker compose run --rm app python client/test_client.py 2
