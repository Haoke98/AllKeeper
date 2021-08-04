from django.urls import path

from .views import *
from .views.views import *

urlpatterns = [
    path('getFilm<int:id>', getFilm),
    path('getOpenid<str:js_code>', getUserOpenid),
    path('getAccessToken', getMiniProgramAccessToken),
    path('getSlider', getSlider),
    path('subscriptionAccessToken', getSubscriptionAccessToken),
    path('buyVIP<str:openid>', buyVIP),
    path('updateUserInfo', updateUserInfo),
    path('UrlRedirector<int:id>', UrlRedirector),
    path('getArticleInfo', getArticleInfo),
    path('getAllArticles', getAllArticles),
    path('videoUrlVid=<int:vid>', videoUrlMaker),
    path('getAllHousesInfo', getAllHousesInfo),
    path('uploadImg', upload_temp_image, name="upload_img"),
    path('deleteImg', delete_img_from_subscriptions, name="delete_img_from_subs"),
    path('updateSystemInfo', updateSystemInfo, name="updateSystemInfo")
]
