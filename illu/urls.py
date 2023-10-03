from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from illu import illus

urlpatterns = [
    path('uploads/',illus.uploadhandler),
    path('pic/',illus.dispatcher)
] 
