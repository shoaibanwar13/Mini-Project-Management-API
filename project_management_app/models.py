from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    ROLE_CHOICES=(
        ('admin','Admin'),
        ('member','Member')

    )
    role=models.CharField(max_length=10,choices=ROLE_CHOICES,default="member")
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True,
        help_text="The groups this user belongs to.",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
    )
class Project(models.Model):
    title=models.CharField(max_length=300)
    description=models.TextField()
    creator=models.ForeignKey(User,on_delete=models.CASCADE,related_name="Project_Assigner")
class Task(models.Model):
    STATUS_CHOICES=(
        ('to_do','To Do'),
        ('in_progress','In Progress'),
        ('completed','Completed')

    )
    title=models.CharField(max_length=300)
    description=models.TextField()
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='to_do')
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name="Project_Tasks")


# Create your models here.
