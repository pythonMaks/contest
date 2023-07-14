from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.task_list, name='task_list'),
    path('tasks_create/', views.task_create, name='task_create'),
    path('task/<slug:slug>/', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/edit/', views.task_edit, name='edit_task'),
    path('submission/<int:pk>/', views.submission_detail, name='submission_detail'),
    path('author/<str:prepod>/', views.author_tasks_view, name='author_tasks'),
    path('tasks/difficulty/<int:difficulty>', views.difficulty_tasks_view, name='difficulty_tasks'),
    path('tasks/language/<str:language>', views.language_tasks_view, name='language_tasks'),
]
