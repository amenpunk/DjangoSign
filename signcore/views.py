from django.shortcuts import render
from rest_framework import viewsets,status
from .serializers import FileSerializer
from .models import File
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from .handleUpload import handle_uploaded_file
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files.storage import default_storage


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all().order_by('name')
    serializer_class = FileSerializer


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, )

    def post(self, request, format='jpg'):
        up_file = request.FILES['file']
        print(up_file)
        file_name = default_storage.save(up_file.name, up_file)
        print(file_name)
        # destination = open('/media/' + up_file.name, 'wb+')
        # for chunk in up_file.chunks():
            # print(chunk)
        # destination.close()  # File should be closed only after all chuns are added

        # ...
        # do some stuff with uploaded file
        # ...
        return Response(up_file.name, status.HTTP_201_CREATED)
# Create your views here.

class ExampleView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        print(render)
        return Response({'received data': request.data})
