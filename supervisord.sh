python manage.py celery worker --loglevel=info -B
gunicorn databaseDemo.wsgi:application -c /home/wsl/mnt/f/wsl/project/databaseDemo/gunicorn.conf.py
