from django.urls import path
from . import views

app_name = 'monitor'

urlpatterns = [
	path('', views.index, name = 'index'),
	path('all_device/', views.all_device, name = 'all_device'),
	path('group/', views.group, name = 'group'),
	path('invent/', views.invent, name = 'invent'),
	path('invent/nb', views.invent, name = 'inventNB'),
	path('invent/pc', views.invent, name = 'inventPC'),
	path('group/group_command', views.group_command, name = 'group_command'),
	path('all_device/sort_all_device', views.sort_all_device, name = 'sort_all_device'),
	path('all_device/save_device', views.save_device, name = 'save_device'),
	path('<int:mikrot_id>/', views.detail, name = 'detail'),
	path('<int:mikrot_id>/view_host/', views.view_host, name = 'view_host'),
	path('<int:mikrot_id>/sort_host/', views.sort_host, name = 'sort_host')
] 
