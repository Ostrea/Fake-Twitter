from django.conf.urls import url

from . import views


app_name = 'twitter_clone_app'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^help/$', views.help, name='help'),
    url(r'^about/$', views.about, name='about')
]
