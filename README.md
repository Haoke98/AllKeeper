<div align="center">
  <img height="320px" src="common-static/img/LOGO.png"/>
  <div>简体中文 | <a href="./README.en.md">English</a></div>
  <p>
    基于Django3.2.7+Vue2+ElementUI的相对比较自动化生成的后台管理系统。借助SimpleUI开源项目对Django原生的Admin后台管理页面进行了二次开发和优化改进而生成的比较现代化的后台管理系统。
  </p>
</div>

## 🌱 运行项目命令
先在izbasar目录下新建一个secret.py文件
```python
_DEBUG = False

SECRET_KEY = ''
ADMIN_PATH = ''
ADMIN_USERNAME = ""
ADMIN_PASSWORD = ""
JWT_SIGNATURE = SECRET_KEY
JWT_ISSUER = ""

ES_USERNAME = ""
ES_PASSWORD = ""
ES_URI = "https://127.0.0.1:9002"
ES_CA = "/usr/etc/http_ca.ctr"

SMTP_EMAIL = ""
SMTP_PASSWORD = ""
```
再执行以下命令来产生数据库文件
```shell
python manage.py makemigrations
python manage.py migrate
```
再执行以下命令来运行项目即可
```bash
# 直接console运行
python manange.py runserver 7000
# 后台运行
nohup python manange.py runserver 7000 > app.log 2>&1 & echo $! > app.pid
```

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
### 问题二：Sqlite版本问题
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
## 感谢巨人

<a title="Python" href="https://www.python.org/" target="_blank">
<img height="100" src="https://www.python.org/static/img/python-logo.png"/>
</a>
<a title="ElasticSearch" href="https://www.elastic.co/cn/" target="_blank">
<img height="100" src="https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt280217a63b82a734/5bbdaacf63ed239936a7dd56/elastic-logo.svg"/>
</a>
<a title="Django" href="https://www.djangoproject.com/" target="_blank">
<img height="100" src="https://pics5.baidu.com/feed/241f95cad1c8a786c081e12fe414593b70cf500f.png?token=f17de3ff5dd522ffb3212ff0f1fe9f9f"/>
</a>
<a title="SimpleUI" href="https://simpleui.72wo.com/docs/simpleui/" target="_blank">
<img height="100" src="https://simpleui.72wo.com/static/images/logo.png"/>
</a>

## 杰出贡献者

<a href="https://gitee.com/sadam98" target="_blank">
  <img width="50px" style="border-radius:999px" src="https://portrait.gitee.com/uploads/avatars/user/1882/5648408_sadam98_1580052770.png!avatar200"/>
</a>

## 联系我们

- 如果二次开发或者部署过程中有什么问题，可以随时联系我们。
<table>
<tr>
<td>
<img width="200px" src="http://59.110.225.84/static/sdm/qr_qq.png">
</td>
</tr>
</table>

## 友情链接
