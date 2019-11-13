from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^wall$', views.wall),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^message/(?P<user_id>\d+)$', views.message),
    url(r'^comment/(?P<user_id>\d+)/(?P<message_id>\d+)$', views.comment),
    url(r'^logout$', views.logout)
]