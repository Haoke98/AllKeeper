# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/9/14
@Software: PyCharm
@disc:
======================================="""
import base64

if __name__ == '__main__':
    encrypted_str = "YnBsaXN0MDDYAQIDBAUGBwgJCQkKCQsMDVZjb3Vyc2VVc3BlZWRTYWx0U2xvbld2ZXJ0QWNjU2xhdFl0aW1lc3RhbXBXaG9yekFjYyMAAAAAAAAAACNAVecImgJ1JSNAReVP3ztkWjNBxUN9UAAAACNAQYAAAAAAAAgZICYqLjY6RExVXmdwAAAAAAAAAQEAAAAAAAAADgAAAAAAAAAAAAAAAAAAAHk="
    content_byte = base64.b64decode(encrypted_str)
    content_str = content_byte.decode("utf-8", errors="ignore")
    print(content_str)
