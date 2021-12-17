"""
Django settings for izBasar project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import mimetypes
import os
import platform
from pathlib import Path

from . import secret

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = Path(__file__).resolve().parent.parent

PUBLIC_ROOT = os.path.join(BASE_DIR, 'public')
if not os.path.exists(PUBLIC_ROOT):
    os.mkdir(PUBLIC_ROOT)

STATIC_URL = '/sdm/static/'
STATIC_ROOT = os.path.join(PUBLIC_ROOT, 'static')
if not os.path.exists(STATIC_ROOT):
    os.mkdir(STATIC_ROOT)

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(PUBLIC_ROOT, 'media')
# if not os.path.exists(MEDIA_ROOT):
#     os.mkdir(MEDIA_ROOT)
#
IMAGE_ROOT = os.path.join(STATIC_ROOT, "img")
if not os.path.exists(IMAGE_ROOT):
    os.mkdir(IMAGE_ROOT)

LOG_FILE_DIR = os.path.join(PUBLIC_ROOT, 'log')
if not os.path.exists(LOG_FILE_DIR):
    os.mkdir(LOG_FILE_DIR)

CACHE_DIR = os.path.join(BASE_DIR, 'cache')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret.SECRET_KEY
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


# SECURITY WARNING: don't run with debug turned on in production!
from . import IS_DEBUG
DEBUG = IS_DEBUG

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
    'simpleui',
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
    'accountSystem',
    'DebtManagerSystem',
    'HousingTransactionSystem'
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

from .secret import DB

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB.MYSQL_DATABASE,
        'USER': DB.MYSQL_USER_NAME,
        'PASSWORD': DB.MYSQL_PASSWORD,
        'PORT': DB.MYSQL_PORT,
        'HOST': DB.MYSQL_HOST,
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

# LANGUAGE_CODE = 'en-us'
#
# USE_TZ = False  # true时统一全球时间，不跨时区的应用可以设为False
# # TIME_ZONE = 'UTC'
# TIME_ZONE = 'Asia/Shanghai'
#
# USE_I18N = True
#
# USE_L10N = True

LANGUAGE_CODE = 'zh-Hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = False
USE_TZ = False

DATETIME_FORMAT = 'Y/m/d H:i:s'

DATE_FORMAT = 'Y/m/d'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
FILE_CHARSET = 'gb18030'
DEFAULT_CHARSET = 'utf-8'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/html', '.html')

# SIMPLE UI config.
SIMPLEUI_DEFAULT_THEME = 'admin.lte.css'

SIMPLEUI_ICON = {
    '所有手机号': 'fab fa-whatsapp',
    '房屋交易系统': 'fas fa-warehouse',
    'Web3Da': 'fas fa-cubes',
    '债务管理及分析系统': 'fas fa-wallet',
    '影院': 'fas fa-film',
    '账号管理系统': 'fas fa-tasks',
    '所有密码': 'fas fa-key',
    'Maps': 'fas fa-map',
    '所有图片': 'fas fa-images',
    '所有电子邮箱': 'fas fa-at',
    '所有语言': 'fas fa-language',
    '用户': 'fas fa-user-shield',
    '所有Film': 'fas fa-film',
    '所有视频': 'fab fa-youtube',
    'Static filess': 'fas fa-folder-open',
    'Settingss': 'fas fa-cogs',
    '所有国家': 'fas fa-globe-asia'
}

SIMPLEUI_LOGO = 'http://59.110.225.84/media/izbasar/logo_square.png'
SIMPLEUI_HOME_INFO = False  # 首页上的simpleUI的版本信息板块。
SIMPLEUI_ANALYSIS = False# 收集信息（TODO：不太好，等正式上线后建议关闭；否则出现信息泄露）
