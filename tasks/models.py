from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Task(models.Model):
    title = models.CharField(max_length = 100 )
    description = models.TextField(null = True)
    create = models.DateTimeField(auto_now_add = True)
    complete_at = models.DateTimeField(null=True)
    important = models.BooleanField(default = False)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    
    def __str__(self) -> str:
        return self.title