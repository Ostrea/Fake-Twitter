from django.conf.urls import url

from . import views


app_name = 'twitter_clone_app'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^help/$', views.help, name='help')
]
