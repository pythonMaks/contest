from django.contrib import admin
from .models import Profile
from .models import User

  
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    list_display = ('username','choice')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Additional Info', {
            'fields': (
                'choice',
                'date',
                'chat_id'
            ),
        }),
        ('Permissions', {
            'fields': ('is_active', ),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User, CustomUserAdmin)