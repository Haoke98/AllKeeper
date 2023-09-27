# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/9/27
@Software: PyCharm
@disc:
======================================="""
import hashlib
import os

if __name__ == '__main__':
    # 生成随机 salt
    salt = os.urandom(16).hex()

    # 用户输入的密码
    password = "sadam98"

    # 将密码和 salt 进行连接
    salted_password = password + salt

    # 对连接后的字符串进行 SHA1 散列计算
    sha1_hash = hashlib.sha1(salted_password.encode()).hexdigest()

    print("Salt:", salt)
    print("Secret (SHA1 Hash):", sha1_hash)
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.ImM2N2VjMzU1NzM5YjU1MzA3MWFkMDMxNGExOTY4NzAyZDljYTE4ZTIi.Q9yr2PSV5uyHyBUwYc4OU_GLH9Z9tmCKgFmNKJfO1qY