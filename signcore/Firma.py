from iota.transaction.validator import SUPPORTED_SPONGE
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse,QueryDict, FileResponse
from rest_framework import viewsets,status
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
from firebase_admin import firestore
from datetime import datetime, timedelta
from iota import Iota, TryteString, Address, Tag, ProposedTransaction
from pprint import pprint
import json

import time

import json

class Firma(APIView):

    def get(self, request):
        try:
            data = QueryDict.dict(request.GET)
            uid = data['uid']
            print(data)

            db = firestore.client()
            sign_ref = db.collection('usersigns').document(uid).collection("signs")
            docs = sign_ref.stream()
            files = []

            for doc in docs:
                dic = doc.to_dict()
                files.append(dic)
            print(files)

            return JsonResponse( { 'status': True, "why" : 'success', 'data' : [] })

        except BaseException as e:
            print(e)
            return JsonResponse( { 'status': False, "why" : e })

    def post(self, request):

        try:

            data=json.loads(request.body)
            print(data)

            uid = data['uid']
            qr = data['hash']
            name = data['name']
            mail = data['mail']

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
            ref_my_sings = db.collection('usersigns').document(uid).collection('signs').document(qr)

            document = {
                'uid' : uid,
                'document' : qr,
                'timestamp' :datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"),
                'name' :  name,
                'mail' :  mail
            }

            to_put = json.dumps(document)

            api = Iota(adapter='https://nodes.devnet.iota.org:443', testnet=True)
            my_data = TryteString.from_unicode(to_put)
            my_address = Address.random(length=81)
            my_tag = Tag(b'SCARLETSIGN')
            tx = ProposedTransaction( address=my_address, value=0, tag=my_tag, message=my_data)
            response = api.send_transfer([tx])
            signature = response['bundle'][0].hash
            document['signature'] = str(signature)
            document['write']  = time.time()

            save = ref.set(document)
            save_my_signs = ref_my_sings.set(document)

            return JsonResponse({ 'status':  True,'head' : 'Excelente!!', 'message' : 'Tu firma fue realizada' })
        except BaseException as e:
            print(e)
            return JsonResponse({ 'status':  False, 'head' : 'Error!!', 'message' : 'Ocurrio un error, intentalo nuevamente' })

