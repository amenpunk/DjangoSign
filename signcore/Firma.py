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
                'timestamp' :datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"),
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
            save = ref.set(document)
            print(save)

            return JsonResponse({ 'status':  True,'head' : 'Excelente!!', 'message' : 'Tu firma fue realizada' })
        except BaseException as e:
            print(e)
            return JsonResponse({ 'status':  False, 'head' : 'Error!!', 'message' : 'Ocurrio un error, intentalo nuevamente' })

