# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/9/8
@Software: PyCharm
@disc:
======================================="""
import sys
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from moviepy.video.io.VideoFileClip import VideoFileClip

if __name__ == '__main__':
    video = VideoFileClip(sys.argv[1])
    # 获取视频的第0秒（即开头）的帧，作为缩略图
    thumbnail = video.get_frame(0)

    # 转换为PIL Image对象
    image = Image.fromarray(thumbnail)

    # 创建一个临时的二进制数据缓冲区
    buffer = BytesIO()
    # 保存缩略图到文件
    # image.save("thumbnail.jpg")
    # 将图像保存到二进制缓冲区
    image.save(buffer, format='JPEG')
    # 创建ContentFile对象
    content_file = ContentFile(buffer.getvalue())
    # 关闭二进制缓冲区
    buffer.close()