from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse,QueryDict
from rest_framework import viewsets,status
from rest_framework.decorators import api_view
import ipfsApi

import os

class API(APIView):

    def get(self, request):
        try:
            data = QueryDict.dict(request.GET)
            print(data)
            uid = data['uid']

            ipfs = ipfsApi.Client('127.0.0.1', 5001)
            doc = ipfs.get(uid)
            print(doc)

            return JsonResponse({ 'status' : True })
        except BaseException as e:
            print(e)
            return JsonResponse({ 'status' : False })

    def post():
        print('ok')
        return HttpResponse('created successfuly')

    @api_view(['GET', 'POST'])
    def hello(request):
        try:
            print('okkk')
            return JsonResponse({ 'status' : True })
        except BaseException as e:
            print(e)
            return JsonResponse({ 'status' : False })
