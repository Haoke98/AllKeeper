import platform

from . import secret
from izBasar.secret import ES_HM194_URI, ES_HM194_USERNAME, ES_HM194_PASSWORD

_DEBUG = False
_STATIC_URL = '/static/'
WINDOWS = 'Windows'
LINUX = 'Linux'
MacOS = 'Darwin'
CURRENT_SYSTEM = platform.system()

if CURRENT_SYSTEM == WINDOWS:
    _DEBUG = True

elif CURRENT_SYSTEM == MacOS:
    _DEBUG = True
    import pymysql

    pymysql.version_info = (1, 4, 13, "final", 0)
    pymysql.install_as_MySQLdb()  # 使用pymysql代替mysqldb连接数据库
else:
    """
        服务器环境 
    """
    _STATIC_URL = '/sdm/static/'
    import pymysql

    pymysql.version_info = (1, 4, 13, "final", 0)
    pymysql.install_as_MySQLdb()  # 使用pymysql代替mysqldb连接数据库
try:
    _DEBUG = secret._DEBUG
except:
    pass
print(f"this app is running on {CURRENT_SYSTEM},DEBUG:{_DEBUG}")
from elasticsearch import Elasticsearch

clientHM194 = Elasticsearch(hosts=ES_HM194_URI, http_auth=(ES_HM194_USERNAME, ES_HM194_PASSWORD),
                            timeout=3600)
