from xml.etree.ElementInclude import include
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('api/matching', views.matching)
]