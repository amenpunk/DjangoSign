from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse, QueryDict
from django.core.files.storage import default_storage
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, MultiPartParser

from .Db import Firestore

import ipfsApi
import io
import time

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

            data = QueryDict.dict(request.POST)

            up_file = request.FILES['file']
            ipfs = ipfsApi.Client('127.0.0.1', 5001)
            hash_info = ipfs.add(up_file)

            signature = hash_info['Hash']
            filename = signature + '.pdf'

            exist = default_storage.exists(filename)

            if not exist:
                default_storage.save(name=filename,content=up_file);

            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            # can.drawString(70, 750, f"DOC-SIGN : <{signature}>")
            can.drawString(0, 0, f"DOC-SIGN : <{signature}>")
            can.save()

            packet.seek(0)
            doc = default_storage.url(filename)
            new_pdf = PdfFileReader(packet)
            existing_pdf = PdfFileReader(open("../signature/"+ doc, "rb"))
            output = PdfFileWriter()
            page = existing_pdf.getPage(0)
            page.mergePage(new_pdf.getPage(0))
            output.addPage(page)

            outputStream = open(filename, "wb")
            output.write(outputStream)
            outputStream.close()

            ### save insert into database
            document = {
                'write' : time.time(),
                'hash' : signature,
                'filename' : data['filename']
            }

            database = Firestore()
            doc_ref = database.db.collection('documents').document(data['uid']).collection('files').document(signature)
            doc_ref.set(document)

            return JsonResponse( { 'status': True, "why" : 'success' }, safe=False)

        except BaseException as e:
            print(e)
            return JsonResponse( { 'status': False, "why" : 'err' }, safe=False)

    def get(self,request):
        try:
            data = QueryDict.dict(request.GET)
            uid = data['uid']
            database = Firestore()
            files_ref = database.db.collection('documents').document(uid).collection('files')
            docs = files_ref.stream()
            files = []

            for doc in docs:
                dic = doc.to_dict()
                files.append(dic)

            return JsonResponse( { 'status': True, "why" : 'success', 'data' : files })
        except BaseException as e:
            print(e)
            return JsonResponse( { 'status': False, "why" : 'error' }, safe=False)

