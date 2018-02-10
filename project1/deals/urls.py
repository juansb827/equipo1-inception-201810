from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^addUser/$', views.add_user, name='addUser'),
    url(r'^logout/$', views.logout_user, name='logout')
]