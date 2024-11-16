# View Database Points
psql -U postgres -d maptest

## Press Enter for password

## View all points
SELECT id, name, description, ST_AsText(location) as location
FROM map_app_point;

# Update Code(if it is not automatically updated on the website)
## First Accept all!
After making code changes in a Django project, you need to follow these steps:
If you modified models (models.py), you need to create and apply database migrations:
http://127.0.0.1:8000/

```python  
conda activate map_env
cd D:\Homeworks\project_map\
# Create migration files
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# If you modified static files (CSS, JavaScript, etc.), collect static files
python manage.py collectstatic

# Restart Django server
python manage.py runserver
```
If your Django project is running, you need to restart the Django server to apply changes:
If using development server (python manage.py runserver),
it usually detects changes and reloads automatically
If in production environment, need to restart web server (like uwsgi or gunicorn)
Clear Python cache files:
Delete all __pycache__ directories and .pyc files
```python
rm -rf __pycache__
rm -rf *.pyc
```
If you're using a caching system, you may need to clear the cache:
```python
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```
Finally, it's recommended to test after applying changes:
```python
python manage.py 
python manage.py shell
```

