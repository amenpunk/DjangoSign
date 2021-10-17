from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse,QueryDict, FileResponse
from rest_framework import viewsets,status
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
from firebase_admin import firestore
import json

class ValideHash(APIView):

    def get(self, request):
        try:
            data = QueryDict.dict(request.GET)
            hash = data['hash']
            db = firestore.client()
            files = []

            file_ref = db.collection('files')
            query_ref = file_ref.where('hash','==', hash ).stream()

            for doc in query_ref:
                print(doc)
                files.append( doc.to_dict()   )

            return JsonResponse( { 'status': True, "why" : 'success', 'data' : files })

        except BaseException as e:
            print(e)
            return JsonResponse( { 'status': False, "why" : e })

    def post(self, request):
        data=json.loads(request.body)
        uid = data['uid']
        # base = data['base64']

        return JsonResponse({ 'status':  True, 'method' : 'POST' })

