from django.conf.urls import patterns, include, url
from myuw_mobile.views.page import index, myuw_login

urlpatterns = patterns('myuw_mobile.views.page',
    url(r'login', 'myuw_login'),
    url(r'support', 'support'),
    url(r'^visual', 'index'),
    url(r'^textbooks', 'index'),
    url(r'^instructor', 'index'),
    url(r'^links', 'index'),
    url(r'^$', 'index'),
)
