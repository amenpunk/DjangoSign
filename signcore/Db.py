import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

class Firestore:
    def __init__(self):
        self.path = os.getcwd()
        self.credentials = credentials.Certificate(self.path+'/signcore/'+'GoogleKey.json')
        firebase_admin.initialize_app(self.credentials)
        self.db = firestore.client()

