from django.conf.urls import patterns, url

from player import views

urlpatterns = patterns('',
    url(r'^$', views.home, name = 'home'),
    url(r'^new/$',views.new, name = 'new'),
    url(r'(?P<pk>\d+)/$',views.detail,name='detail'),
)
