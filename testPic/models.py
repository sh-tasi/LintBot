from django.db import models

# Create your models here.
class Pic(models.Model):
    userID=models.CharField(max_length=20, null=False, unique=True)
    userPicUrl=models.CharField(max_length=100, blank=True)