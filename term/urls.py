from django.conf.urls import patterns, url

from term import views

urlpatterns = patterns('',
    url(r'^$', views.home, name = 'home'),
    url(r'^new/$',views.new, name = 'new'),
)
