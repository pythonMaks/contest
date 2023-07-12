from django.contrib import admin
from .models import Task, Test, Submission

admin.site.register(Test)
admin.site.register(Submission)

  

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description',Task.get_language, 'prepod')
