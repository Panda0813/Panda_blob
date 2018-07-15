from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from mainapp import views
from mainapp.views import *

urlpatterns = [
    # url(r'^user/$',views.User_list),
    # url(r'^user/$',UserListView.as_view()),  #关联restful和api
    # url(r'^user/(?P<id>[0-9]+)/$',UserView.as_view()),
    url(r'^$',views.home,name='home'),
    url(r'regist',RegisterView.as_view(),name='regist'),
    url(r'login',LoginView.as_view(),name='login'),
    url(r'vcode',views.vCode,name='vcode'),
    url(r'upload',views.upload),
    url(r'uname/(?P<name>\w+)/$',views.uName),
    url(r'verify/(?P<code>[0-9a-zA-Z]+)/$',views.verifycode),
    url(r'logout',views.logout),
    url(r'addblob',views.addBlob),
    url(r'blob',BlobView.as_view(),name='blob'),
    url(r'show/(?P<blob_id>\d+)$',views.show),
    url(r'replay',views.replay),
    url(r'allreply/(?P<blob_id>\d+)/(?P<num>\d+)$',views.allreply),
]
