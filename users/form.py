from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import SelectDateWidget
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset
from django import forms
from datetime import datetime, timedelta

default_date = datetime.now() - timedelta(days=365 * 18)

class UserRegisterForm(UserCreationForm):    
    date = forms.DateField(widget=SelectDateWidget( attrs={'class': 'my-widget-class'}, years=range(timezone.now().year - 100, timezone.now().year + 1)),
                                 label='Дата рождения', initial=default_date)
    
    
    class Meta:
        model = User                
        fields = ['username', 'password1', 'password2', 'date']
        

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'language']
        
    languages = (('python','Python'), ('kotlinc','Kotlin'), ('node','JavaScript'),('javac', 'Java'))
    language = forms.ChoiceField(choices = languages, label= 'Язык')
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сохранить'))
        self.helper.layout = Layout(
            Fieldset(
                'Изменить информацию профиля',                
                'first_name',
                'last_name',
                'language'
            ),
        )