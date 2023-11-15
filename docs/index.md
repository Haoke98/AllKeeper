<div align="center">
  <img height="320px" src="common-static/img/LOGO.png"/>
  <div>简体中文 | <a href="./README.en.md">English</a></div>
  <p>
    基于Django3.2.7+Vue2+ElementUI的相对比较自动化生成的后台管理系统。借助SimpleUI开源项目对Django原生的Admin后台管理页面进行了二次开发和优化改进而生成的比较现代化的后台管理系统。
  </p>
</div>

![](https://pypi-camo.global.ssl.fastly.net/ecfc98443cb0f8b613316d9004fbcf6d09fb1481/68747470733a2f2f68616f6b6539382e6769746875622e696f2f446a616e676f4173796e6341646d696e2f7374617469632f6469676974616c5f776f726c645f62616e6e65722e706e67)

## 模块&功能

本项目总共有六大模块组成.其分别是：

### 1. 万能堡垒

* 服务器管理
* 宝塔管理
* 内网穿透管理

### 2. 账号管理

* 通用账号管理
* 平台管理

### 3. icloud管理


### 4. 媒体库
* 媒体存储媒体

### 5. 社工库

### 6. 资金管理

## 依赖

### 1. ffmpeg

为了实现icloud相关功能需要安装

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

MEDIA_ROOT = "/home/media"
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
### Nginx 配置实现媒体文件的缩略图功能
nginx 下载地址 http://nginx.org/en/download.html

编译参数：--with-http_image_filter_module
```editorconfig
http{
    ...
    server{
        ...
        location /icloud-shortcut {
            video_thumb;
            image_filter resize 100 200;
            image_filter_jpeg_quality 80;
            alias /external/SADAM/icloud/photos;
            autoindex on;
        }
        location /icloud {
            alias /external/SADAM/icloud/photos;
            autoindex on;
        }
        ...
    }
    ...
}
```
### 配置系统服务并开启自启动
先创建allkeeper.service文件并复制allkeeper.service.sample的内容
```shell
cp allkeeper.service.sample allkeeper.service
```
再修改内容, 再移到系统服务单位存储目录
```shell
vi allkeeper.service
mv allkeeper.service /usr/lib/systemd/system/
```
加载新加入的服务单位
```shell
systemctl daemon-reload
```
启动服务
```shell
systemctl start allkeeper.service
```
开启开机自启动
```shell
systemctl enable allkeeper.service
```

### 开启数据库定时备份
#### 1. 首先，创建一个备份脚本（例如：backup_mysql.bat（Windows）或backup_mysql.sh（Linux）），包含以下内容：

Windows脚本（backup_mysql.bat）：
```shell
@echo off
For /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
For /f "tokens=1-2 delims=/:" %%a in ("%TIME%") do (set mytime=%%a%%b)
set mydatetime=%mydate%_%mytime%
set BackupFile=backup_directory\backup_%mydatetime%.sql
"mysql_install_directory\bin\mysqldump.exe" -u USERNAME -pPASSWORD DATABASE_NAME > %BackupFile%
```
Linux脚本（backup_mysql.sh）：
```shell
#!/bin/sh
script_path="$(dirname "$(readlink -f "$0")")"
echo "当前脚本所在路径：$script_path"
backup_dir=${script_path}/backup_sql
mkdir -p $backup_dir
mysqldump -u all_keeper -p 1_nDb9tk0pwa all_keeper > ${backup_dir}/all-keeper_`date +%Y%m%d%H%M%S`.sql
```
将backup_directory替换为您想存储备份文件的目录

将mysql_install_directory替换为MySQL安装目录

使用真实的数据库用户名代替USERNAME

使用真实的数据库密码代替PASSWORD

使用要备份的数据库名称代替DATABASE_NAME

#### 2. 为脚本设置可执行权限（仅在Linux上需要）：
```shell
chmod +x backup_mysql.sh
```
#### 3. 创建一个定时任务（Windows Task Scheduler或Linux的cron）：
a) Windows定时任务：

打开任务计划程序
单击"创建基本任务"，然后设置触发器（例如：每天、每周等），并选择刚创建的备份脚本作为要执行的操作。

b) Linux的cron任务：

在终端中键入crontab -e以编辑cron配置
添加以下内容（根据实际情况修改）：
```shell
0 2 * * * /path/to/backup_mysql.sh
```
这将在每天凌晨2点执行备份任务。请将/path/to替换为脚本的实际路径。


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
