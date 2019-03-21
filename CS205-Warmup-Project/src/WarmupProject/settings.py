import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

USE_TZ = True
TIME_ZONE = "UTC"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

INSTALLED_APPS = (
    'db',
)

# SECURITY WARNING: Modify this secret key if using in production!
SECRET_KEY = '2nl^4muny^-3bpinpe899q1wixz0*y&fy%8hiy78xgp=amu_=9'

# APP SETINGS
CSV_FILE_PATH = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../../Data/AirBnb Listings/amsterdam_listings_v0.csv"))

