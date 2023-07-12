from django.shortcuts import render, redirect
from django.contrib import messages
from .form import UserRegisterForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from .models import User
from core.models import Submission, Task
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():            
            form.save()
            username = form.cleaned_data.get('username')
            
            messages.success(request, f'Создан аккаунт {username}!')
            return redirect('blog-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
        

@login_required
def profile(request):
    user = request.user
    user_form = UserProfileForm(instance=user)
    password_form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        if 'password_change' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Пароль изменён!')
        else:
            user_form = UserProfileForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Ваш профиль был обновлен.')
    
    student_submission = Submission.objects.filter(student=request.user.username)
    prepod_task = Task.objects.filter(prepod=request.user.username)
    return render(request, 'users/profile.html',{'student_submission': student_submission,
                                                'prepod_task': prepod_task,
                                                'user_form': user_form,
                                                'password_form': password_form
                                                })
@login_required
def delete_task(request, pk):
    task = Task.objects.get(pk=pk)       
    task.delete()
    messages.success(request, 'Задача была успешно удалена.')
    return redirect('catalog')