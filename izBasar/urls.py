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
from django.contrib import admin
from django.contrib.flatpages import sitemaps
from django.contrib.sitemaps.views import sitemap
from django.urls import path, re_path
# from django.contrib.staticfiles.views import serve
from django.views.generic import RedirectView
from django.views.static import serve

import accountSystem.urls
from izBasar import settings
from . import _STATIC_URL
from .secret import ADMIN_PATH

admin.autodiscover()

urlpatterns = [
    path(ADMIN_PATH, admin.site.urls),
    # re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    # url('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    re_path('^all-keeper/', include(accountSystem.urls)),
    path("favicon.ico", RedirectView.as_view(url=_STATIC_URL + 'favicon.ico')),
    re_path(r'^static/(?P<path>.*)$', serve, ({'document_root': settings.STATIC_ROOT}))
]
