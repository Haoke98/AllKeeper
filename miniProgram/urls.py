from django.urls import path

from .views import getAllKino

urlpatterns = [
    path('getKino<int:id>', getAllKino),
]
