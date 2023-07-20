from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import SelectDateWidget
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset
from django import forms
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

default_date = datetime.now() - timedelta(days=365 * 18)

def validate_latin_chars(value):
    if not re.match(r'^[a-zA-Z]+$', value):
        raise ValidationError(
            _("Имя пользователя необходимо писать латинскими буквами."),
            code='invalid'
        )
        
class UserRegisterForm(UserCreationForm):    
    date = forms.DateField(widget=SelectDateWidget( attrs={'class': 'my-widget-class'}, years=range(timezone.now().year - 100, timezone.now().year + 1)),
                                 label='Дата рождения', initial=default_date)
    show_password1 = forms.BooleanField(required=False, label='Показать пароль')
    show_password2 = forms.BooleanField(required=False, label='Показать пароль')
    username = forms.CharField(validators=[validate_latin_chars])
    class Meta:
        model = User                
        fields = ['username', 'password1', 'show_password1', 'password2', 'show_password2', 'date']

    
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