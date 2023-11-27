# 数据迁移教程

## db-migrate （实验🧪：失败❌）

1. 配置

```json
{
  "src": {
    "migrationDirectory": "migrations",
    "driver": "mysql",
    "host": "localhost",
    "port": 3306,
    "database": "example",
    "user": "root",
    "password": "root",
    "multipleStatements": true
  },
  "dst": {
    "migrationDirectory": "migrations",
    "driver": "pg",
    "host": "localhost",
    "port": 5432,
    "database": "example",
    "user": "postgres",
    "password": "postgres",
    "multipleStatements": true
  }
}
```

2. 运行命令：

```shell
db-migrate up --config migrate-config.json --env src dst
```

## pgloader (实验🧪:成功✅)

查询版本:

```shell
docker run --rm -it dimitri/pgloader:latest pgloader --version
```

帮助文档：

```shell
docker run --rm -it dimitri/pgloader:latest pgloader --help
docker run --rm -it dimitri/pgloader:latest pgloader --with --help
```

### 从其他数据库迁移数据到PostgreSQL

#### 从MySQL迁移数据

```shell
docker run --rm -it dimitri/pgloader:ccl.latest pgloader --with "quote identifiers" mysql://user:password@localhost:port/database_name postgresql://user:password@host:port/database_name
```

#### 遇到的问题

##### 1. Heap exhausted during garbage collection:

该问题出现在最新版本(202311271215), 所以只要把版本改成ccl.latest即可, [详细请见](https://github.com/dimitri/pgloader/issues/962).

### 其他

* 文档和教程：[详见Pgloader官方文档](https://pgloader.readthedocs.io/en/latest/tutorial/tutorial.html#)
* GitHub源码地址：[dimitri/pgloader](https://github.com/dimitri/pgloader)