from django.urls import re_path
from rest_framework.routers import DefaultRouter

from .views import preview, sync_progress, test, count, thumb, detail,upload_file

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
                  re_path('preview', preview),
                  re_path('sync_progress', sync_progress),
                  re_path('test', test),
                  re_path('total', count),
                  re_path('thumb', thumb),
                  re_path('upload', upload_file),
                  # # re_path('^human$', HumanView.as_view()),
                  # re_path('^images/thumbnail', image.thumbnail, name='thumbnail'),
                  # re_path('^images', image.image_view),
                  # re_path('^breath', breath.BreathView),
                  # path('getSubcribtionAccessToken', getSubcribtionsAccessToken),
                  # path('buyVIP<str:openid>', buyVIP)
              ] + router.urls
