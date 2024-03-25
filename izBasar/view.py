# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/3/19
@Software: PyCharm
@disc:
======================================="""
from django.core.files.storage import default_storage
from django.http import FileResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required


@login_required
def media(request, path: str):
    """
    通过default_storage获取MinioStorage上的media资源再用视图返回给用户
    :param request: 请求实例
    :param path: 文件路径
    FIXME : 延迟很长, 需要做缓存
    """
    file_name = path
    # 检查文件是否存在
    if default_storage.exists(file_name):
        # 打开文件
        with default_storage.open(file_name, 'rb') as file:
            # 创建一个文件响应对象并返回
            response = FileResponse(file)
            # 设置内容类型
            response['Content-Type'] = 'application/octet-stream'
            return response
    else:
        # 文件不存在，可以返回404错误或其他响应
        return HttpResponseNotFound(f'The file[{path}] does not exist')
