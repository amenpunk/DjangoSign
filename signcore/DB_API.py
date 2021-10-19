from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse,QueryDict, FileResponse
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
import ipfsApi

from firebase_admin import firestore
import json

class API(APIView):

    def get(self, request):
        try:

            data = QueryDict.dict(request.GET)
            hash = data['hash']
            db = firestore.client()

            ref = db.collection('firmas').document(hash).collection('users')
            docs = ref.stream()
            files = []

            for doc in docs:
                dic = doc.to_dict()
                files.append(dic)

            return JsonResponse( { 'status': True, "why" : 'success', 'data' : files })


        except BaseException as e:
            print(e)
            return JsonResponse({ 'status' : False })
    # def get(self, request):
    #     try:
    #         data = QueryDict.dict(request.GET)
    #         print(data)
    #         file_name = data['id']
    #         print(file_name)
    #         pdf = os.getcwd() + default_storage.url(f'{file_name}.pdf')
    #         response = FileResponse(open(pdf, 'rb'))
    #         return response
    #     except BaseException as e:
    #         print(e)
    #         return JsonResponse({ 'status' : False })

    def post():
        print('ok')
        return HttpResponse('created successfuly')

