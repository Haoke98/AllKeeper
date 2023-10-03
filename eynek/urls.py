from django.urls import re_path
from rest_framework.routers import DefaultRouter

from .views import proxy

router = DefaultRouter()
urlpatterns = [
    re_path('proxy/(?P<api_path>.+)/$', proxy),

]
