from django.db import models


# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=512)
    email = models.EmailField()
    status = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
