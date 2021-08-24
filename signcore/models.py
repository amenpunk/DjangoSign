from django.db import models

class File(models.Model):
    name = models.CharField(max_length=60)
    url = models.CharField(max_length=60)
    def __str__(self):
        return self.name

class Document(models.Model):
    docfile = models.FileField(upload_to='documents')

# Create your models here.
