from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse,QueryDict, FileResponse
from rest_framework import viewsets,status
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
from firebase_admin import firestore
from datetime import datetime, timedelta
import json

class Firma(APIView):

    def get(self, request):
        try:
            data = QueryDict.dict(request.GET)
            uid = data['uid']
            hash = data['hash']
            # db = firestore.client()

            # sign_ref = db.collection('signature').document(uid)
            # doc = sign_ref.get()
            # files = doc.to_dict()

            return JsonResponse( { 'status': True, "why" : 'success', 'data' : [] })

        except BaseException as e:
            print(e)
            return JsonResponse( { 'status': False, "why" : e })

    def post(self, request):

        try:
            data=json.loads(request.body)
            print('rece -> ', data)
            uid = data['uid']
            qr = data['hash']
            db = firestore.client()


            ### find if already exist
            doc_ref = db.collection('firmas').document(qr).collection('users').document(uid)
            doc = doc_ref.get()

            if doc.exists:
                print('Documento ya existe')
                return JsonResponse({ 'status':  True, 'head' : 'Ups!!' ,'message' : 'Ya has firmado este documento' })
            else:
                print(u'No such document!')

            ref = db.collection('firmas').document(qr).collection('users').document(uid)

            document = {
                'uid' : uid,
                'document' : qr,
                'timestamp' :datetime.now(),
            }

            save = ref.set(document)
            print(save)

            return JsonResponse({ 'status':  True,'head' : 'Excelente!!', 'message' : 'Tu firma fue realizada' })
        except BaseException as e:
            print(e)
            return JsonResponse({ 'status':  False, 'head' : 'Error!!', 'message' : 'Ocurrio un error, intentalo nuevamente' })

