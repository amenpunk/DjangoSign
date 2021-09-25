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
from firebase_admin import firestore
import base64
import locale
from datetime import datetime, timedelta


import ipfsApi
import io
import os
import time

from firebase_admin import firestore

class IPFS(APIView):
    parser_classes = (MultiPartParser,)
    def post (self, request, format='pdf'):
        try:

            dt = datetime.now()
            db = firestore.client()
            now = str(time.time())

            data = QueryDict.dict(request.POST)
            print('DATA -> ', data)
            print(request.FILES['file'])
            filename = now + '.pdf'
            Image = None
            Sign = int(data['sign'])

            if Sign == 1:
                ref = db.collection('signature').document(data['uid'])
                doc = ref.get()
                if doc.exists:
                    base = doc.to_dict()
                    Image = base['image']
                    decodeit = open(now+'.png', 'wb')
                    decodeit.write(base64.b64decode((Image)))
                    decodeit.close()
                else:
                    print(u'No such document!')


            packet = io.BytesIO()
            redeable  = dt.strftime("%A %d de %B del %Y - %H:%M")
            can = canvas.Canvas(packet, pagesize=letter)
            can.setFont("Times-Roman", 15)

            can.drawString(20, 600, f"UID : <{ data['uid'] }>")
            can.drawString(20, 630, f"TIMESTAMP : <{ now }>")
            can.drawString(20, 660, f"DATE : <{ redeable }>")
            can.drawString(20, 690, f"SERVER TIMESTAMP: <{ datetime.now() }>")
            can.drawString(20, 720, f"FILENAME : <{ data['filename']  }>")

            if Sign and Image:
                can.drawImage(image=now + '.png', x=20, y=0, width=200, height=300)
                can.line(x1=43,y1=50, x2=250,y2=50)
                can.drawString(x=30, y=50,text="F ")

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
                'timestamp' :datetime.now(),
                'hash' : signature,
                'filename' : data['filename'],
            }

            db = firestore.client()

            doc_ref = db.collection('documents').document(data['uid']).collection('files').document(signature)
            save = doc_ref.set(document)

            print(save)
            if Image:
                os.remove( now + ".png" )

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

