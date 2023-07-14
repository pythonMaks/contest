from django.shortcuts import render, redirect
from .forms import GroupForm
from django.contrib.auth.decorators import login_required


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
