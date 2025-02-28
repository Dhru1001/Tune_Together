from django.urls import path
from api.views import *

urlpatterns = [
    path("backend", backend, name="backend"),
]
