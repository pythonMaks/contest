from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from core.models import Submission, Task
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from users.models import User



class MyDetailView(DetailView):
    model = Submission # название класса из models.py
    template_name = 'catalog/detail.html'
    context_object_name = 'article' # что-нибудь логичное
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.object.task  # получаем объект Task, связанный с Submission
        context['task_name'] = task.name  # добавляем имя Task в контекст
        return context  
      
@login_required
def index(request):
    user = request.user     
    prepod_task = Task.objects.filter(prepod=user.username)
    article = Submission.objects.filter(student=user.username)
    return render(request, 'catalog/catalog.html',{
                                                'prepod_task': prepod_task, 
                                                'article': article                                               
                                                })



@login_required
def students_list(request, task_id):   
    students_unique = Submission.objects.filter(prepod=request.user.username, task__id=task_id).values('student').distinct()
    return render(request, 'catalog/students_list.html', {'students': students_unique, 'task_id': task_id})

@login_required
def submission_list(request, student, task_id):   
    submission = Submission.objects.filter(prepod=request.user.username, student=student, task__id=task_id)
    return render(request, 'catalog/submission_list.html', {'submission': submission, 'task_id': task_id})
