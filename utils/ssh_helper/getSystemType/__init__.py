# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/7/26
@Software: PyCharm
@disc:
======================================="""
import paramiko


def getSystemType(client: paramiko.SSHClient) -> str:
    std_in, std_out, str_err = client.exec_command("lsb_release -a")
    if str_err.readable():
        for err in str_err.readlines():
            print(err)
    else:
        for line in std_out.readlines():
            print(line)


def getSystemType(client):
    pass
