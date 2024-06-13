from .common import *

DEBUG = False
SECRET_KEY = env.str('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

LOCKDOWN_PASSWORDS = env('LOCKDOWN_PASSWORDS')

DATABASES = {
    "default": env.db("DATABASE_URL")
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

MEDIA_ROOT = env('MEDIA_ROOT', default=BASE_DIR / 'media')
MEDIA_URL = env('MEDIA_URL', default='/media/')
