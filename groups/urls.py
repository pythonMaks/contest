from django.urls import path
from . import views

urlpatterns = [
    path('group/', views.create_group, name='create_group'),
   
]
