from django.urls import path
from . import views

urlpatterns = [
	path('', views.welcomePage),
	path('company', views.companyPage),
path('user', views.userPage),
	
	path('sample/test_data', views.send_testGraphData)
]
