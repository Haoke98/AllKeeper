<div align="center">
  <img height="320px" src="common-static/img/LOGO.png"/>
  <div>简体中文 | <a href="./README.en.md">English</a></div>
  <p>
    基于Django3.2.7+Vue2+ElementUI的相对比较自动化生成的后台管理系统。借助SimpleUI开源项目对Django原生的Admin后台管理页面进行了二次开发和优化改进而生成的比较现代化的后台管理系统。
  </p>
</div>

## 🌱 运行项目命令

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
