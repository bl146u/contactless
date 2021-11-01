run: collectstatic
	uvicorn config.asgi:application --host 192.168.1.101 --port 8099

development: collectstatic
	uvicorn config.asgi:application --reload --debug --host 192.168.1.101 --port 8099

collectstatic:
	./manage.py collectstatic --noinput
