from django.conf.urls import patterns, url

from game import views

urlpatterns = patterns('',
    url(r'^$', views.home, name = 'home'),
    url(r'^(?P<pk>\d+)/$',views.detail,name='detail'),
    url(r'^(?P<gpk>\d+)/player/(?P<ppk>\d+)/$',views.player_game,name='new game'),
)
