python manage.py celery worker --loglevel=info
gunicorn databaseDemo.wsgi:application -c /home/wsl/mnt/f/wsl/project/databaseDemo/gunicorn.conf.py
