from django.contrib import admin
from .models import Task, Test

admin.register(Test)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description',Task.get_language, 'prepod')
