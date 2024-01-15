from rest_framework import viewsets
from rest_framework.views import APIView

from accountSystem.pagination import StandardPagination
from utils.http_helper import RestResponse
from ..models import ServerNew
from ..serializers import ServerSerializer


class ServerView(APIView):

    def get(self, request, format=True):
        serverObjsQS = ServerNew.objects.all()
        # return RestResponse(200, "OK", pagination.page(page))
        pagination = StandardPagination()
        # pagination = PageNumberPagination()
        # pagination.page = 1
        # pagination.page_size = 10
        ret = pagination.paginate_queryset(serverObjsQS, request)
        serializer = ServerSerializer(ret, many=True)
        return RestResponse(200, "ok", serializer.data)


class ServerViewSet(viewsets.ModelViewSet):
    queryset = ServerNew.objects.all()
    serializer_class = ServerSerializer
    pagination_class = StandardPagination
