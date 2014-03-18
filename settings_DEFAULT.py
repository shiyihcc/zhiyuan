# Settings for Zhiyuan based site.
# -*- coding: UTF-8 -*-

DEBUG = False
TEMPLATE_DEBUG = DEBUG
STATIC_PATH = './static'

SITE_NAME = "[志愿]"
BASE_URL = "http://zhiyuan.shiyiquan.cn/"

# also in base.html
TEST_HOST = "z.hcc.im"

MAIL_NOTIFICATION = True

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dbname',                      # Or path to database file if using sqlite3.
        'USER': 'dbuser',                      # Not used with sqlite3.
        'PASSWORD': 'dbpassword',              # Not used with sqlite3.
        'HOST': 'dbhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': 'dbport',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = None

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
STATIC_ROOT = '/var/quan/zhiyuan/static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
STATIC_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'miaowmiaowmiaowww!!!'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

DATE_FORMAT = 'Y年n月j日\nH:i'

import os.path
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
)

INSTALLED_APPS = (
    'zy',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.markup',
)
