from django.shortcuts import render
from rest_framework import viewsets,status
from .serializers import FileSerializer
from .models import File
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from .forms import UploadFileForm
from .handleUpload import handle_uploaded_file
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files.storage import default_storage
import ipfsApi
import json


def log(js):
    json_object = json.loads(js)
    json_formatted_str = json.dumps(json_object, indent=2)
    print(json_formatted_str)

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

    def post(self, request, format='pdf'):
        try:



            up_file = request.FILES['file']
            print(up_file)
            file_name = default_storage.save(up_file.name, up_file)
            print(file_name)
            return Response(up_file.name, status.HTTP_201_CREATED)
        except BaseException as e:
            print(f'error {e}')


def IpCheck(request):
    # ipfs.io/ipfs/hash
    try:
        ipfs = ipfsApi.Client('127.0.0.1', 5001)
        doc = default_storage.open('spider_white.jpg')
        ip = ipfs.add(doc)
        print(ip)
        res = { "status" : True }
        return JsonResponse(res, safe=False)
    except BaseException as e:
        print('api error -> ', e)
        return HttpResponse(f'error {e}')

class IPFS(APIView):
    parser_classes = (MultiPartParser,)
    def post (self, request, format='pdf'):
        try:
            up_file = request.FILES['file']
            ipfs = ipfsApi.Client('127.0.0.1', 5001)
            ip = ipfs.add(up_file)
            print(ip)
            return JsonResponse( { 'status': True, "why" : 'success' }, safe=False)
        except BaseException as e:
            return JsonResponse( { 'status': False, "why" : e }, safe=False)

