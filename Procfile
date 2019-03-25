web: sh -c 'cd server && daphne server.asgi:application --port $PORT --bind 0.0.0.0 -v2'
worker: sh -c 'cd server && python manage.py runworker channels -v2'