from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets,status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import UserRateThrottle
from firebase_admin import firestore

import os

class API(APIView):

    def get(self, request):
        try:
            dbv = firestore.client()
            doc = {
                'first': 'ming',
                'last': 'mecca',
                'born': 1815
            }
            doc_ref = database.db.collection('document').add(doc)
            print(doc_ref)
            return JsonResponse({ 'status' : True })
        except BaseException as e:
            print(e)
            return JsonResponse({ 'status' : False })

    def post():
        print('ok')
        return HttpResponse('created successfuly')

    @api_view(['GET', 'POST'])
    def hello(request):
        data = request.data
        print(data['test'])
        return HttpResponse('created successfuly')


