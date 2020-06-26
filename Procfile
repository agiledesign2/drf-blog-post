release: python manage.py migrate --settings=website.settings.prod
web: gunicorn website.wsgi --log-file -
