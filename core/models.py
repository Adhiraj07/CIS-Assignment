from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

ROLES= (
    ('ADMIN','Admin'),
    ('MANAGER','Manager'), 
    ('USER','User'),
)

TASK_STATUS= (
    ('PENDING','Pending'),
    ('IN_PROGRESS','In-Progress'), 
    ('COMPLETED','Completed'),
    ('MISSED','Missed'),
)

class User(AbstractUser):
    role= models.CharField(max_length=50,choices=ROLES,default='USER')
    last_deactivation= models.DateTimeField(null=True,blank=True)
    is_active= models.BooleanField(default=True)
    
    def __str__(self):
        return self.username

class Task(models.Model):
    title= models.CharField(max_length=250)
    description= models.TextField()
    deadline= models.DateField()
    status= models.CharField(max_length=50,choices=TASK_STATUS,default='PENDING')
    assigned_to = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tasks')
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='assigned_tasks',on_delete=models.SET_NULL,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.status}"
