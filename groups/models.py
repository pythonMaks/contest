from django.db import models
from core.models import Task
from django.conf import settings

class Group(models.Model):
    professor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='taught_groups')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, through='GroupMembership')
    name = models.CharField(max_length=255)
    tasks = models.ManyToManyField(Task)

    def __str__(self):
        return self.name

class GroupMembership(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'group',)

    def __str__(self):
        return f'{self.student.username} in {self.group.name}'

class TaskGrade(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    grade = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.student.username} - {self.task.name} - {self.grade}'
