## 常见问题
### 问题一:下拉框选择列表获取失败
现在Windows上执行一下命令
```shell
python3 manage.py collectstatic
```
然后执行一下命令
```shell
scp -rC /Users/shadikesadamu/Projects/izbasar/django-admin/public root@192.168.1.100:/root/AllKeeper/
```
### 问题二：Sqlite版本异常1
> 异常：django.core.exceptions.ImproperlyConfigured: SQLite 3.9.0 or later is required (found 3.7.17).

解决方案：
1. 首先检查确认现有版本：
```shell
sqlite3 --version
```
2. 其次安装正确版本的sqlite（如报错提示，必须大于等于3.9.0)
![](assets/20221227015348.jpg)
从SQLite官网下载最新版本的软件包
```shell
wget https://www.sqlite.org/2022/sqlite-autoconf-3400000.tar.gz
tar -xvzf sqlite-autoconf-3400000.tar.gz 
cd sqlite-autoconf-3400000.tar.gz
./configure
make && make install
echo export LD_LIBRARY_PATH="/usr/local/lib">> ~/.bashrc
```

### 问题三：Sqlite3版本异常2
> 异常：django.db.utils.NotSupportedError: deterministic=True requires SQLite 3.8.3 or higher
> 
> 升级了 sqlite 版本（因 django 怕改动太大就没有尝试卸载django重新安装的方法）。
如下，明明版本已经更新成最新了环境变量也加了，软链接指向也是最新了，可运行还是提醒版本过低。
> 
> 可能是不支持新的版本，最终决定更换sqlite3 为pysqlite3 和 pysqlite3-binary

解决方案：
1. 安装pysqlite3和pysqlite3-binary
```shell
pip install pysqlite3
pip install pysqlite3-binary
```
2. 打开文件/usr/local/python3/lib/python3.8/site-packages/django/db/backends/sqlite3/base.py，找到 from sqlite3 import dbapi2 as Database 注释它，添加代码
```python
#from sqlite3 import dbapi2 as Database  #注释它
from pysqlite3 import dbapi2 as Database #新加这段代码
```