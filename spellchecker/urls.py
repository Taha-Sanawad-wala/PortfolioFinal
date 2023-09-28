from django.contrib import admin
from django.urls import path
from spellchecker.views import index,spell,grammar

urlpatterns = [
    path('',index),
    path('spell/',spell),
    path('grammar/',grammar),
]
