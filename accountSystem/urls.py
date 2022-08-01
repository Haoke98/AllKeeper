from django.urls import re_path
from rest_framework.routers import DefaultRouter

from .views import ServerViewSet, login, getMenuList, DeviceViewSets

router = DefaultRouter()
router.register(r'server', viewset=ServerViewSet)
router.register(r'device', viewset=DeviceViewSets)
# server_list = ServerViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# server_detail = ServerViewSet.as_view({
#     'get': 'retrieve'
# })
urlpatterns = [
                  # re_path('^servers/$', server_list),
                  # re_path('^server/(?P<pk>[0-9]+)$', server_detail),
                  re_path('^login$', login),
                  re_path('^system/menu$', getMenuList),
                  # path('getAccessToken', getAccessToken),
                  # path('getSlider', getSlider),
                  # path('getSubcribtionAccessToken', getSubcribtionsAccessToken),
                  # path('buyVIP<str:openid>', buyVIP)
              ] + router.urls
