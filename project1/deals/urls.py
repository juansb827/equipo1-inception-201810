from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^addUser/$', views.add_user, name='addUser'),
    url(r'^editUser/$', views.edit_user, name='editUser'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^addComment/$', views.add_comment, name='addComment')
]