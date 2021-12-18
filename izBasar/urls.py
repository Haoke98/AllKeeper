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
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
# from django.contrib.staticfiles.views import serve
from django.views.static import serve

admin.autodiscover()
from django.contrib.flatpages import sitemaps
from django.contrib.sitemaps.views import sitemap
from django.urls import path

import BeansMusic.urls
import WEB3DA.urls
import miniProgram.urls
from izBasar import settings
from miniProgram.views import image
from .secret import ADMIN_PATH
from django.urls import re_path
urlpatterns = [
                  path(ADMIN_PATH, admin.site.urls),
                  # re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
                  # url('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
                  path('miniProgram/', include(miniProgram.urls)),
                  path('W3DA/', include(WEB3DA.urls)),
                  path('admin/doc/', include('django.contrib.admindocs.urls')),
                  path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
                       name='django.contrib.sitemaps.views.sitemap'),
                  path('BeansMusic/', include(BeansMusic.urls)),
                  path('image/proxy', image.proxy)
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)