# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2022/11/4
@Software: PyCharm
@disc:
======================================="""
from rest_framework import viewsets
from rest_framework.views import APIView

from utils.http_helper import RestResponse
from ..models import Human
from ..pagination import StandardPagination
from ..serializers import HumanSerializer


class HumanView(APIView):

    def get(self, request, format=True):
        humanObjsQS = Human.objects.all()
        # return RestResponse(200, "OK", pagination.page(page))
        pagination = StandardPagination()
        # pagination = PageNumberPagination()
        # pagination.page = 1
        # pagination.page_size = 10
        ret = pagination.paginate_queryset(humanObjsQS, request)
        serializer = HumanSerializer(ret, many=True)
        return RestResponse(200, "ok", serializer.data)


class HumanViewSet(viewsets.ModelViewSet):
    queryset = Human.objects.all()
    serializer_class = HumanSerializer
    pagination_class = StandardPagination
#
