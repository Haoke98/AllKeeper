"""izBasar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.flatpages import sitemaps
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views import static
from django.views.static import serve

import BeansMusic.urls
import WEB3DA.urls
import miniProgram.urls
from izBasar import settings
from miniProgram.views import image

urlpatterns = [
    # path('admin/sadaaasdfjkaljskldjf12sadf34e12kdfjxkljkljfklqwxsdkl/', admin.site.urls),
    path('admin/', admin.site.urls),
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    path('miniProgram/', include(miniProgram.urls)),
    url('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    url('^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    path('W3DA/', include(WEB3DA.urls)),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('BeansMusic/', include(BeansMusic.urls)),
    path('image/proxy', image.proxy)
]
