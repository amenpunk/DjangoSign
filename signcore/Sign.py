from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse,QueryDict, FileResponse
from rest_framework import viewsets,status
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
from firebase_admin import firestore
import json

class Sign(APIView):

    def get(self, request):
        try:
            data = QueryDict.dict(request.GET)
            uid = data['uid']
            db = firestore.client()

            sign_ref = db.collection('signature').document(uid)
            doc = sign_ref.get()
            files = doc.to_dict()

            return JsonResponse( { 'status': True, "why" : 'success', 'data' : files })

        except BaseException as e:
            print(e)
            return JsonResponse( { 'status': False, "why" : e })

    def post(self, request):
        data=json.loads(request.body)
        uid = data['uid']
        base = data['base64']

        document = {
            'uid' : uid,
            'image' : base,
        }

        db = firestore.client()
        doc_ref = db.collection('signature').document(uid)
        save = doc_ref.set(document)
        print(save)

        return JsonResponse({ 'status':  True, 'method' : 'POST' })

