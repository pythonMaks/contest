from django import forms
from .models import Submission, Task, Test
from crispy_forms.layout import Submit, Layout, Fieldset
from crispy_forms.helper import FormHelper
from groups.models import TaskGrade

class TaskGradeForm(forms.ModelForm):
    class Meta:
        model = TaskGrade
        fields = ['grade']



class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['code']
        widgets = {
            'code': forms.Textarea(attrs={'rows': 10}),
        }
        


class TaskForm(forms.ModelForm):
    name = forms.CharField(label='Название')
    LANGUAGES = (('python', 'Python'), ('kotlinc', 'Kotlin'), ('node', 'JavaScript'), ('java', 'Java'))
    language = forms.ChoiceField(choices = LANGUAGES, label= 'Язык')
    description = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'rows': 10}))
    difficulty = forms.ChoiceField(choices = Task.DIFFICULTY_CHOICES, label='Сложность')
    class Meta:
        model = Task
        fields = ['language', 'name', 'description', 'difficulty']

    def __init__(self, *args, **kwargs):
        user_language = kwargs.pop('user_language', 'python')
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['language'].initial = user_language
        self.fields['language'].choices = self.LANGUAGES

        
class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['input', 'output']
        widgets = {
            'input': forms.Textarea(attrs={'rows': 3}),
            'output': forms.Textarea(attrs={'rows': 3}),
        }

TestFormSet = forms.inlineformset_factory(Task, Test, form=TestForm, extra=1)

