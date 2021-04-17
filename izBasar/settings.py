"""
Django settings for izBasar project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
LOG_FILE_DIR = os.path.join(STATIC_ROOT, 'log')
if not os.path.exists(LOG_FILE_DIR):
    os.mkdir(LOG_FILE_DIR)
CACHE_DIR = os.path.join(STATIC_ROOT, 'cache')
res = os.path.join(BASE_DIR, os.path.pardir)
outerFolder = os.path.abspath(res)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's3va_7)!ovu!=3j55p2m9@yk0h4-w!l9&v&m#9-(9xduye*@p='
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
import platform

WINDOWS = 'Windows'
LINUX = 'Linux'
SADAM_SET = {
    "DEBUG": False,
    "BASE_HREF": "BASE_HREF_TWO_PLATFORMS",
}
if platform.system() == WINDOWS:
    SADAM_SET["DEBUG"] = False
    SADAM_SET["BASE_HREF"] = "http://10.128.202.191:7000"
else:
    SADAM_SET["DEBUG"] = False
    SADAM_SET["BASE_HREF"] = "https://x.izbasarweb.xyz"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = SADAM_SET.get("DEBUG")

ALLOWED_HOSTS = ['*']

APPEND_SLASH = True

ADMINS = (('Sadam·Sadik', '1903249375@qq.com'), ('Haoke98', 'kws11@qq.com'), ('!', 'callme_0920@qq.com'))  # 接受报错的账号
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.qq.com'  # 如果是 163 改成 smtp.163.com
EMAIL_PORT = 465
EMAIL_HOST_USER = ADMINS[2][1]  # 帐号
EMAIL_HOST_PASSWORD = "bhwuenurolvldjga"  # 密码(用第三方平台登陆授权码）
SERVER_EMAIL = EMAIL_HOST_USER  # 必须要设置 不然logger中得handler：admin_Email 无法发送错误报告邮件，  SERVER_EMAIL必须和 EMAIL_HOST_USER一样才能成功发送
DEFAULT_FROM_EMAIL = 'SadamSadik <1903249375@qq.com>'

#########################
## Django Logging  BEGIN
#########################

# LOGGING_DIR 日志文件存放目录
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(levelname)s [%(asctime)s] [%(request_id)s] %(filename)s-%(funcName)s-%(lineno)s: %(message)s'
            # 这里使用filter request_id里的request_id字段
        },
        'default': {
            'format': '%(levelname)s [%(asctime)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',  # 这里使用上面的formatter: standard
        },
        'file': {  # 记录到日志文件(需要创建对应的目录，否则会出错)
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_FILE_DIR, 'debug.log'),  # 日志输出文件
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份份数
            'formatter': 'default',  # 使用哪种formatters日志格式
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,

        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],  # 这里使用上面的handler: console
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False
        },
        'project.app': {
            'handlers': ['file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True
        }
    }
}
#########################
## Django Logging  END
#########################
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'miniProgram',
    'WEB3DA',
    'django.contrib.admindocs',
    'django.contrib.sitemaps',
    'BeansMusic',
    'accountSystem'
]
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
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'izBasar.middleware.sadam_middleware'
]

ROOT_URLCONF = 'izBasar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'izBasar.wsgi.application'

import configparser

cf = configparser.ConfigParser()
cf.read(os.path.join(BASE_DIR, os.path.join('izbasar', 'secret.conf')))

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': cf.get('db', "MYSQL_DATABASE"),
        'USER': cf.get('db', "MYSQL_USER_NAME"),
        'PASSWORD': cf.get('db', "MYSQL_PASSWORD"),
        'PORT': cf.get('db', "MYSQL_PORT"),
        'HOST': cf.get('db', "MYSQL_HOST"),
    }
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

LANGUAGE_CODE = 'en-us'

USE_TZ = False  # true时统一全球时间，不跨时区的应用可以设为False
# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
