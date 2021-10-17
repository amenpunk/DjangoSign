from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse,QueryDict, FileResponse
from rest_framework import viewsets,status
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage

import ipfsApi

import os

class API(APIView):

    def get(self, request):
        try:
            data = QueryDict.dict(request.GET)
            print(data)
            file_name = data['id']

            ipfs = ipfsApi.Client('127.0.0.1', 8080)
            content =  ipfs.cat(file_name)
            file_response = FileResponse(content)
            print('response -> ', file_response)
            # print(file_name)
            # pdf = os.getcwd() + default_storage.url(f'{file_name}.pdf')
            # response = FileResponse(open(content, 'rb'))
            # return JsonResponse({ 'status' : True })
        except BaseException as e:
            print('ERROR -> ',e)
            return JsonResponse({ 'status' : False })

    def post():
        print('ok')
        return HttpResponse('created successfuly')

