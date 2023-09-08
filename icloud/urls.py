from django.urls import re_path
from rest_framework.routers import DefaultRouter

from .views import detail,sync_progress

router = DefaultRouter()
# router.register(r'server', viewset=ServerViewSet)
# router.register(r'human', viewset=HumanViewSet)
# server_list = ServerViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# server_detail = ServerViewSet.as_view({
#     'get': 'retrieve'
# })
urlpatterns = [
                  re_path('detail', detail),
                  re_path('sync_progress', sync_progress),
                  # # re_path('^server/(?P<pk>[0-9]+)$', server_detail),
                  # re_path('^login$', login),
                  # re_path('^system/menu$', getMenuList),
                  # # re_path('^human$', HumanView.as_view()),
                  # re_path('^images/thumbnail', image.thumbnail, name='thumbnail'),
                  # re_path('^images', image.image_view),
                  # re_path('^breath', breath.BreathView),
                  # path('getSubcribtionAccessToken', getSubcribtionsAccessToken),
                  # path('buyVIP<str:openid>', buyVIP)
              ] + router.urls
