from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import urls
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    url(r'^log_out/$', views.log_out, name='log_out'),
    path('', views.welcomePage),
    path('company', views.companyPage),
    path('company/new', views.newCompany, name='new_company'),
    path('company/shares/<int:id>', views.editCompanyShares, name='edit_shares'),
    path('shares', views.myShares, name='view_shares'),
    path('user', views.userPage, name='user'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('user/companies', views.myCompanies, name='user_companies'),
    path('signup', views.signup),
    path('sample/test_data', views.send_testGraphData),
]
