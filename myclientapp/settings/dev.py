from .common import *
#environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

ALLOWED_HOSTS = ['*']
DEBUG = True
SECRET_KEY = 'django-insecure-cirz^#=8zk8$+goq3nc3@7j_4bt0p^fmw6k+kp=4dx6z!b8pc4'
WHITENOISE_AUTOREFRESH = True
LOCKDOWN_ENABLED = False
# LOCKDOWN_PASSWORDS = env('LOCKDOWN_PASSWORDS')

DATABASES = {
    "default": env.db("DATABASE_URL")
    # "default": "postgres://tutorial:tutorial@db/tutorial"
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': '<tutorial>',
    #     'USER': 'postgres',
    #     'PASSWORD': 'tutorial',
    #     'HOST': '0.0.0.0',
    #     'PORT': '5432',
    # }
}