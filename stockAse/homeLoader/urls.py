from django.urls import path
from . import views

urlpatterns = [
	path('', views.welcomePage),
	path('sample/test_data', views.send_testGraphData)
]
