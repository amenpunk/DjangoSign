from django.db import models

class File(models.Model):
    name = models.CharField(max_length=60)
    url = models.CharField(max_length=60)
    def __str__(self):
        return self.name

# Create your models here.
