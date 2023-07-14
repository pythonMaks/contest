from django.urls import path
from . import views

urlpatterns = [
    path('group/', views.create_group, name='create_group'),
    path('groups/', views.view_groups, name='groups'),
    path('group/<int:group_id>/', views.view_group, name='group_detail'),
   
]
