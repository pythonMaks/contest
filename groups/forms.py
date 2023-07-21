from django import forms
from .models import Group
from users.models import User
from core.models import Task
from django_select2.forms import Select2MultipleWidget

class GroupForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(choice='1'),  # выбираем только студентов
        widget=Select2MultipleWidget,    
        required=True,
        label='Студенты'
    )
    tasks = forms.ModelMultipleChoiceField(
        queryset=Task.objects.none(),  # пустой queryset по умолчанию
        widget=Select2MultipleWidget,        
        required=True,
        label='Задачи'
    )

    class Meta:
        model = Group
        fields = ['name', 'students', 'tasks']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(GroupForm, self).__init__(*args, **kwargs)
        if user:
            # если пользователь - преподаватель, показываем только его задачи
            self.fields['tasks'].queryset = Task.objects.filter(prepod=user.username)
