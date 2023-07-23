from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.contenttypes.models import ContentType
from contest import settings
from django.utils.text import slugify
from django.urls import reverse
from core.models import Submission
import random
import string
# group = Group.objects.create(name='Teachers')
# permission = Permission.objects.get(codename='can_create_task')
# group.permissions.add(permission)

class User(AbstractUser):
    choice = models.CharField( max_length=150, default=1, blank=True, verbose_name='Статус', help_text='1 - Студент, 2 - Преподаватель, 3 - Администратор')
    date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    slug = models.SlugField(null=False, blank=True, unique=True)
    prepopulated_fields = {'slug': ('username',)}
    language = models.CharField(("language"), max_length=150, blank=True)
    access_code = models.CharField(max_length=32, blank=True, null=True)
    chat_id = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        permissions = (("can_create_task", "Can create task"),)
    def save(self, *args, **kwargs):
        if not self.access_code:
            self.access_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        self.slug = slugify(self.username)
        if self.choice == '3':
            # assign permission to manage users
            self.is_staff = True 
            self.is_superuser = True  
                 
           
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse("mydetail", kwargs={"slug": self.slug})    

    def has_submission_for(self, task):
        return Submission.objects.filter(task=task, student=self.username).exists()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    def __str__(self):
        return f'{self.user.username} Profile'



