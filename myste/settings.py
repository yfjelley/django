# coding: utf-8
import os
"""
Django settings for myste project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ct#trhaf61e@*s(cqtbhn^cdu68ous^uo!qd$8p75ny@4@$ji9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'opt',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'myste.urls'

WSGI_APPLICATION = 'myste.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysite',
        'USER': 'root',
        'PASSWORD': '123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
DEFAULT_CHARSET='utf-8'

STATIC_ROOT="/usr/local/lib/python2.7/dist-packages/django/bin/myste"
STATIC_URL = '/static/'
STATICFILES_DIRS = (
            os.path.join(STATIC_ROOT, "static"),
            )

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },
    'filters': {
        'require_debug_true':{
            '()':'django.utils.log.RequireDebugTrue',
            }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters':['require_debug_true'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'default': {
            'level':'DEBUG',
            'filters':['require_debug_true'],
            'class':'logging.handlers.RotatingFileHandler',
#            'filename': '/usr/local/lib/python2.7/dist-packages/django/bin/myste/all.log', #或者直接写路径：'filename':'c:\logs\request.log''  
            'filename': os.path.join(STATIC_ROOT+'/logs/','all.log'), #或者直接写路径：'c:\logs\all.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'console':{
            'level': 'DEBUG',
            'filters':['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level':'DEBUG',
            'filters':['require_debug_true'],
            'class':'logging.handlers.RotatingFileHandler',
#            'filename': '/usr/local/lib/python2.7/dist-packages/django/bin/myste/all.log', #或者直接写路径：'filename':'c:\logs\request.log''  
            'filename': os.path.join(STATIC_ROOT+'/logs/','script.log'), #或者直接写路径：'filename':'c:\logs\request.log''  
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'scprits_handler': {
            'level':'DEBUG',
            'filters':['require_debug_true'],
            'class':'logging.handlers.RotatingFileHandler',
#            'filename': '/usr/local/lib/python2.7/dist-packages/django/bin/myste/all.log', #或者直接写路径：'filename':'c:\logs\request.log''  
            'filename': os.path.join(STATIC_ROOT+'/logs/','script.log'), #或者直接写路径：'filename':'c:\logs\script.log'
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default','console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'XieYin.app':{
            'handlers': ['default','console'],
            'level': 'DEBUG',
            'propagate': True         
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
        'scripts': { # 脚本专用日志
            'handlers': ['scprits_handler'],
            'level': 'INFO',
            'propagate': False
        },
    }
}          

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STSTATIC_ROOTATIC_URL = '/static/'
