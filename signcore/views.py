from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse, QueryDict
from django.core.files.storage import default_storage
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, MultiPartParser
from django.core.files import File

import ipfsApi
import io
import os
import time

from firebase_admin import firestore

class IPFS(APIView):
    parser_classes = (MultiPartParser,)
    def post (self, request, format='pdf'):
        try:

            now = str(time.time())

            data = QueryDict.dict(request.POST)
            print(request.FILES['file'])
            filename = now + '.pdf'

            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.setFont("Times-Roman", 15)
            can.setFillColor('red')
            # can.drawString(70, 750, f"DOC-SIGN : <{signature}>")
            can.drawString(10, 500, f"DOC-SIGN : <{ filename  }>")
            can.save()

            packet.seek(0)
            new_pdf = PdfFileReader(packet)
            existing_pdf = PdfFileReader( request.FILES['file']   )

            if new_pdf.isEncrypted:
                new_pdf.decrypt('')

            if existing_pdf.isEncrypted:
                existing_pdf.decrypt('')

            # file_string = io.BytesIO()

            merge = PdfFileMerger()
            merge.append(existing_pdf)
            merge.append(new_pdf)
            merge.write(filename)
            # merge.write(file_string)

            # djang_new_pdf = File(file_string, filename)
            # default_storage.save(name=filename,content=djang_new_pdf);

            # doc = default_storage.url(filename)

            ipfs = ipfsApi.Client('127.0.0.1', 5001)
            hash_info = ipfs.add(filename)
            print('IPFS response -> ',hash_info)
            os.remove(filename)
            signature =  hash_info['Hash']

            ### save insert into database
            document = {
                'write' : time.time(),
                'hash' : signature,
                'filename' : data['filename']
            }

            db = firestore.client()

            doc_ref = db.collection('documents').document(data['uid']).collection('files').document(signature)
            save = doc_ref.set(document)
            print(save)

            return JsonResponse( { 'status': True, "why" : 'success', "data" : document }, safe=False)

        except BaseException as e:
            print(e)
            return JsonResponse( { 'status': False, "why" : e }, safe=False)

    def get(self,request):
        try:
            data = QueryDict.dict(request.GET)
            uid = data['uid']
            db = firestore.client()
            files_ref = db.collection('documents').document(uid).collection('files')
            docs = files_ref.stream()
            files = []

            for doc in docs:
                dic = doc.to_dict()
                files.append(dic)

            return JsonResponse( { 'status': True, "why" : 'success', 'data' : files })
        except BaseException as e:
            print(e)
            return JsonResponse( { 'status': False, "why" : 'error' }, safe=False)

