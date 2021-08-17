from django.shortcuts import render
from rest_framework import viewsets
from .serializers import FileSerializer
from .models import File


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all().order_by('name')
    serializer_class = FileSerializer

# Create your views here.
