from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import urls
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    url(r'^log_out/$', views.log_out, name='log_out'),
    path('', views.welcomePage),
    path('company', views.companyPage),
    path('user', views.userPage),
    path('account/', include('django.contrib.auth.urls')),
    path('signup', views.signup),
    path('sample/test_data', views.send_testGraphData),
]
