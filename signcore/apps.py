from django.apps import AppConfig
import firebase_admin
from firebase_admin import credentials
import os


class SigncoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'signcore'
    cred = credentials.Certificate(os.getcwd() + "/signcore/GoogleKey.json")
    firebase_admin.initialize_app(cred)

