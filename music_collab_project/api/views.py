from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def backend(request):
    return HttpResponse("<h1>Backend</h1>")