

# Create your models here.
from django.db import models

class Movie(models.Model):
    name = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

