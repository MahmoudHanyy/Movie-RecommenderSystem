from django.conf.urls import url, include
from . import views

app_name = 'movies' #used in index.html music:detail Vid #21

urlpatterns = [
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^logout/$', views.userLogout, name='logout'),  # as function
    url(r'^list/$', views.userRecommend, name='list'),
    url(r'^userschoices/$', views.userBased, name='userschoices'),
    url(r'^simusers/$', views.similarUsers, name='simUsers'),
    url(r'^$', views.myindex, name='myindex'), #kolooooo
    url(r'^(?P<pk>\d+)/', views.details, name='details'),
    url(r'^usersearch/(?P<pkuser>\d+)/', views.usersearch, name='usersearch'),
]
