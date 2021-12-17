import platform

IS_DEBUG = False
WINDOWS = 'Windows'
LINUX = 'Linux'
MacOS = 'Darwin'
CURRENT_SYSTEM = platform.system()

if CURRENT_SYSTEM == WINDOWS:
    IS_DEBUG = True

elif CURRENT_SYSTEM == MacOS:
    IS_DEBUG = True
    import pymysql

    pymysql.version_info = (1, 4, 13, "final", 0)
    pymysql.install_as_MySQLdb()  # 使用pymysql代替mysqldb连接数据库
else:
    import pymysql

    pymysql.version_info = (1, 4, 13, "final", 0)
    pymysql.install_as_MySQLdb()  # 使用pymysql代替mysqldb连接数据库
print(f"this app is running on {CURRENT_SYSTEM},DEBUG:{IS_DEBUG}")
