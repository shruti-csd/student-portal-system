from django.db import models

from django.contrib.auth.models import User

# Create your models here.
#user updates the notes and once deleted it deletes everything hence foreign key with cascade used
class Notes(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=20,default="shruti")
    description=models.TextField(default='shruti')
    
    class Meta:
        verbose_name='notes'
        verbose_name_plural='notes'
        
class Homework(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.CharField(max_length=50)
    title=models.CharField(max_length=30)
    description=models.CharField(default='enter',max_length=50)
    due=models.DateTimeField()
    is_finished=models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.title
    
class Todo(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=30, default='enter')
    is_finished=models.BooleanField(default=False)
    
    

