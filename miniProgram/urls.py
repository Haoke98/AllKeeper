from django.urls import path

from .views import *

urlpatterns = [
    path('getFilm<int:id>', getFilm),
    path('getOpenid<str:js_code>', getUserOpenid),
    path('getAccessToken', getAccessToken),
    path('getSlider', getSlider),
    path('getSubcribtionAccessToken', getSubcribtionsAccessToken)
]
