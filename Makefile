run: collectstatic
	uvicorn config.asgi:application --port 8099

development: collectstatic
	uvicorn config.asgi:application --reload --debug --port 8099

collectstatic:
	./manage.py collectstatic --noinput
