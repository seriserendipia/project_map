INSTALLED_APPS = [
    # ...
    'django.contrib.gis',
    'leaflet',
    'map_app',
]

# Database configuration for PostGIS
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'your_db_name',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Leaflet Configuration
LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (0.0, 0.0),
    'DEFAULT_ZOOM': 2,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 18,
} 