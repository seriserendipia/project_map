import os
from pathlib import Path
import logging
from django.core.exceptions import ImproperlyConfigured
import django

print(f"Using Django version: {django.get_version()}")

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
)

# GDAL environment variables setup
if os.name == 'nt':  # Windows system
    OSGEO4W = r"C:\OSGeo4W"
    if os.path.isdir(OSGEO4W):
        # Set environment variables
        os.environ['OSGEO4W_ROOT'] = OSGEO4W
        os.environ['GDAL_DATA'] = OSGEO4W + r"\apps\gdal\share\gdal"
        os.environ['PROJ_LIB'] = OSGEO4W + r"\share\proj"
        
        # Add OSGeo4W bin directory to PATH
        os.environ['PATH'] = OSGEO4W + r"\bin;" + os.environ['PATH']

        # Set GDAL library paths
        GDAL_LIBRARY_PATH = OSGEO4W + r'\bin\gdal309.dll'
        GEOS_LIBRARY_PATH = OSGEO4W + r'\bin\geos_c.dll'

        # Set GDAL version
        os.environ['GDAL_VERSION'] = '3.6.2'

        print("=== GDAL Configuration ===")
        print(f"GDAL_LIBRARY_PATH: {GDAL_LIBRARY_PATH}")
        print(f"GEOS_LIBRARY_PATH: {GEOS_LIBRARY_PATH}")
        print(f"GDAL_DATA: {os.environ.get('GDAL_DATA')}")
        print(f"PROJ_LIB: {os.environ.get('PROJ_LIB')}")
        print(f"PATH: {os.environ.get('PATH')}")
        print("========================")

        # Verify GDAL availability
        try:
            from osgeo import gdal
            print(f"GDAL Version: {gdal.__version__}")
        except ImportError as e:
            print(f"Error importing GDAL: {e}")
            raise ImproperlyConfigured("GDAL Python bindings not available")

# Ensure BASE_DIR is correctly set
BASE_DIR = Path(__file__).resolve().parent.parent

# Add simple logging configuration for testing
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'maptest',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'OPTIONS': {
            'connect_timeout': 10,
            'client_encoding': 'UTF8',
            'sslmode': 'disable',
            'options': '-c search_path=public,postgis'
        },
    }
}

# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Template settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DEBUG = True
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '[::1]',
    '*'  # Use in development only, not recommended for production
]

# Ensure these applications are installed
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',  # GIS functionality
    'leaflet',            # Leaflet maps
    'map_app',           # Your application
    "django_browser_reload",
]

# Leaflet configuration
LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (34.0522, -118.2437),  # Los Angeles coordinates
    'DEFAULT_ZOOM': 12,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 18,
}

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

# Secret key configuration
SECRET_KEY = 'your-secret-key-here'  # Replace with your actual secret key

# Basic settings
USE_I18N = True
USE_TZ = True
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # Use in development only
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:9000",
    "http://127.0.0.1:9000",
]

# Security settings
SECURE_PROXY_SSL_HEADER = None
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

# Debug settings
DEBUG = True
TEMPLATE_DEBUG = True

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'django_debug.log',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Default primary key field type setting
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'