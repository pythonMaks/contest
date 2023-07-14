from django.shortcuts import render, redirect
from .forms import GroupForm
from .models import Group, TaskGrade
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, user=request.user)
        if form.is_valid():
            group = form.save(commit=False)
            group.professor = request.user
            group.save()
            form.save_m2m()
            return redirect('groups')  # имя URL-шаблона для страницы со списком групп
    else:
        form = GroupForm(user=request.user)
    return render(request, 'groups/create_group.html', {'form': form})

@login_required
def view_groups(request):
    groups = Group.objects.filter(professor=request.user)
    return render(request, 'groups/groups.html', {'groups': groups})




@login_required
def view_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    
    # Проверяем, является ли пользователь профессором для этой группы
    if request.user != group.professor:
        return redirect('groups')

    students_grades = []
    for student in group.students.all():
        grades = {}
        for task in group.tasks.all():
            task_grade = TaskGrade.objects.filter(student=student, task=task).first()
            grades[task] = task_grade.grade if task_grade else 0
        students_grades.append((student, grades))

    return render(request, 'groups/view_group.html', {'group': group, 'students_grades': students_grades})
