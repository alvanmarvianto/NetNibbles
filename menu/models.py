from django.db import models
from django.utils.text import slugify
import os

class Menu(models.Model):
    name      = models.CharField(max_length=100)
    category  = models.CharField(max_length=100)
    price     = models.IntegerField()
    desc      = models.TextField()
    image     = models.ImageField(upload_to='images/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
		    return self.name