# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/7/25
@Software: PyCharm
@disc:
======================================="""
import paramiko

from .getSystemType import getSystemType


def ssh_client_con(hostname, port: int = 22, username: str = "root",
                   password: str = "123456") -> paramiko.SSHClient | Exception:
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh_client.connect(hostname=hostname, port=port, username=username, password=password)
        return ssh_client
    except Exception as error:
        return error


if __name__ == '__main__':
    client = ssh_client_con(hostname="218.31.113.194", password="hmxw123456")
    sysType = getSystemType(client)
