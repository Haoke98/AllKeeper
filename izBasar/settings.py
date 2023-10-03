"""
Django settings for izBasar project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import datetime
import logging
import mimetypes
import os
import platform
from pathlib import Path

from . import secret
from .simpleUISettings import *

CSRF_TRUSTED_ORIGINS = ['http://keeper.sdm.net', 'http://kept.sdm.net']
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'none'
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent

LOG_FILE_DIR = os.path.join(BASE_DIR, 'log')
if not os.path.exists(LOG_FILE_DIR):
    os.mkdir(LOG_FILE_DIR)
CACHE_DIR = os.path.join(BASE_DIR, 'cache')

PUBLIC_ROOT = os.path.join(BASE_DIR, 'public')
if not os.path.exists(PUBLIC_ROOT):
    os.mkdir(PUBLIC_ROOT)

from . import _STATIC_URL

STATIC_URL = _STATIC_URL
logging.info(f"STATIC_URL:{STATIC_URL}")
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_ROOT = os.path.abspath(os.path.join(SITE_ROOT, '../'))
STATIC_ROOT = os.path.join(PUBLIC_ROOT, 'static')
print("SITE_ROOT:", SITE_ROOT)
print("STATIC_ROOT:", STATIC_ROOT)
STATICFILES_FINDERS = ("django.contrib.staticfiles.finders.FileSystemFinder",
                       "django.contrib.staticfiles.finders.AppDirectoriesFinder")
# 静态资源目录列表
# 注：当DEBUG=True时，Django将为开发环境提供静态资源服务，该服务将从这些文件夹中搜取静态资源。
# 注：当DEBUG=False时，Django将不会再启动静态资源，如果启动了静态资源，也将会从STATIC__ROOT文件夹中搜取静态资源。
# 注：当执行python manage.py collectstatic 命令时，将把STATICFILES__DIR中的所有静态资源复制到STATIC__ROOT中去
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'accountSystem/static'),
    os.path.join(BASE_DIR, 'common-static'),
    os.path.join(BASE_DIR, 'icloud/static'),
    os.path.join(BASE_DIR, 'eynek/static'),
]
print("STATICFILES_DIR:", STATICFILES_DIRS)

if not os.path.exists(STATIC_ROOT):
    os.mkdir(STATIC_ROOT)

MEDIA_URL = '/media/'
MEDIA_ROOT = secret.MEDIA_ROOT

IMAGE_ROOT = os.path.join(MEDIA_ROOT, "img")
if not os.path.exists(IMAGE_ROOT):
    os.mkdir(IMAGE_ROOT)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret.SECRET_KEY
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

# SECURITY WARNING: don't run with debug turned on in production!
from . import _DEBUG

DEBUG = _DEBUG

ALLOWED_HOSTS = ['*']

APPEND_SLASH = True

ADMINS = (('Sadam·Sadik', '1903249375@qq.com'),)  # 接受报错的账号
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.qq.com'  # 如果是 163 改成 smtp.163.com
EMAIL_PORT = 465
EMAIL_HOST_USER = secret.SMTP_EMAIL  # 帐号
EMAIL_HOST_PASSWORD = secret.SMTP_PASSWORD  # 密码(用第三方平台登陆授权码）
SERVER_EMAIL = EMAIL_HOST_USER  # 必须要设置 不然logger中得handler：admin_Email 无法发送错误报告邮件，  SERVER_EMAIL必须和 EMAIL_HOST_USER一样才能成功发送
DEFAULT_FROM_EMAIL = f'SadamSadik <{secret.SMTP_EMAIL}>'

LOG_REQUEST_ID_HEADER = "HTTP_X_REQUEST_ID"
GENERATE_REQUEST_ID_IF_NOT_IN_HEADER = True
REQUEST_ID_RESPONSE_HEADER = "RESPONSE_HEADER_NAME"

########### Django Logging  BEGIN ##############
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter'
        },
        'new_add': {
            '()': 'middlewares.RequestLogFilter',
        },

    },
    'formatters': {
        'standard': {
            # 这里使用filter request_id里的request_id字段
            'format': '[{asctime:s}][{levelname:^7s}][{processName:s}({process:d}):{threadName:s}({thread:d})][{source_ip}][{hostname}][{request_id}][{filename:s}:{lineno:d}:{funcName:s}]{message:s}',
            'style': '{',
        },
        'default': {
            'format': '%(levelname)s [%(asctime)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['new_add', 'request_id'],
            'formatter': 'standard',  # 这里使用上面的formatter: standard
        },
        'file': {  # 记录到日志文件(需要创建对应的目录，否则会出错)
            'level': 'INFO',
            'filters': ['new_add', 'request_id'],
            'filename': os.path.join(LOG_FILE_DIR, 'AllKeeper.log'),  # 日志输出文件
            'formatter': 'standard',  # 使用哪种formatters日志格式
            'backupCount': 100,  # 备份份数
            'encoding': 'utf-8',

            # 按照时间切割
            'class': 'izBasar.log.CommonTimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,

            # 按照文件大小切割
            # 'class': 'logging.handlers.RotatingFileHandler',
            # 'maxBytes': 1024 * 1024 * 5,  # 文件大小
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,

        }
    },
    'root': {
        'handlers': ['console', 'file', 'mail_admins'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],  # 这里使用上面的handler: console
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False
        },
        'icloud': {
            'handlers': ['file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}
##############    Django Logging  END   ##############


# Application definition
INSTALLED_APPS = [
    'simplepro',
    'simpleui',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'revproxy',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'django.contrib.sitemaps',
    'rest_framework',
    'docutils',
    'accountSystem',
    'DebtManagerSystem',
    'photologue',
    'sortedm2m',
    'django_crontab',
    'icloud',
    'logAnalyser',
    'eynek'
]
SITE_ID = 1
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': CACHE_DIR,
        'TIMEOUT': 600,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}
MIDDLEWARE = [
    'log_request_id.middleware.RequestIDMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middlewares.RequestLogMiddleware',
    'middlewares.AuthCheck',
    # 加入simplepro的中间件
    'simplepro.middlewares.SimpleMiddleware'
]

ROOT_URLCONF = 'izBasar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # <-需要这一行
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'izBasar.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': secret.MYSQL_DATABASE,
        'HOST': secret.MYSQL_HOST,
        'PORT': secret.MYSQL_PORT,
        'USER': secret.MYSQL_USERNAME,
        'PASSWORD': secret.MYSQL_PASSWORD,
        'CONN_MAX_AGE': 0,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
    }
}

DATABASE_ROUTERS = ['izBasar.database_router.DatabaseAppsRouter']
DATABASE_APPS_MAPPING = {
    'core': 'default',
    'admin': 'default',
    'auth': 'default',
    'contenttypes': 'default',
    'sessions': 'default',
    'sites': 'default',
    'accountSystem': 'default',
    'DebtManagerSystem': 'default',
    'icloud': 'default',
    'logAnalyser': 'default'
}
# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = 'zh-Hans'  # 'en-us'
TIME_ZONE = 'Asia/Shanghai'  # 'UTC'
USE_I18N = True
USE_L10N = False
USE_TZ = True  # true时统一全球时间，不跨时区的应用可以设为False

DATETIME_FORMAT = 'Y/m/d H:i:s'

DATE_FORMAT = 'Y/m/d'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
FILE_CHARSET = 'gb18030'
DEFAULT_CHARSET = 'utf-8'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

mimetypes.add_type('text/css', '.css')
mimetypes.add_type('text/css', '.min.css')
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/html', '.html')

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "accountSystem.pagination.StandardPagination",
    "PAGE_SIZE": 10
}

JWT_EXPIRED_DELTA = datetime.timedelta(hours=1)
