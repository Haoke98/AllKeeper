# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/7/26
@Software: PyCharm
@disc:
======================================="""
from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 50
    page_size_query_param = 'pageSize'
    page_size_query_description = "单个页面能够显示的item的数量"
    page_query_param = 'page'
    page_query_description = '页码'

    def get_paginated_response(self, data):
        body = {
            "code": 200,
            "message": "OK",
            "data": {
                "total": self.page.paginator.count,
                "page": self.page.number,
                "pageSize": self.get_page_size(self.request),
                "summary": 0,
                "rows": data
            }
        }
        respList = [
            ('total', self.page.paginator.count),
            ('page', self.page.number),
            ('pageSize', self.get_page_size(self.request)),
            ('hasPrevious', self.page.has_previous()),
            ('hasNextPage', self.page.has_next()),
            ('hasOtherPages', self.page.has_other_pages()),
            ('links', OrderedDict([
                ('prev', self.get_previous_link()),
                ('next', self.get_next_link()),
            ])),
            ('rows', data)
        ]
        if self.page.has_next():
            respList.append(('nextPage', self.page.next_page_number()))
        if self.page.has_previous():
            respList.append(('previousPage', self.page.previous_page_number()))
        return Response(body)
