from django.urls import path
from . import views

app_name = 'monitor'

urlpatterns = [
	path('', views.index, name = 'index'),
	path('<int:mikrot_id>/', views.detail, name = 'detail'),
	path('<int:mikrot_id>/view_host/', views.view_host, name = 'view_host')
] 
