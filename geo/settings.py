DEBUG=True
SECRET_KEY = 'NOT YET SET'
DEBUG = True
ROOT_URLCONF = 'geo.urls'
TEMPLATE_DIRS = ['.']
INSTALLED_APPS = (
	'restless',
)

SRID = 27700

DATABASES = {
    'default': {
         'ENGINE': 'django.contrib.gis.db.backends.postgis',
         'NAME': 'geotest',
         'USER': 'richardpope',
     }
}