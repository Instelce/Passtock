from django.urls import path
from .views import *

app_name = 'password'
urlpatterns = [
    path('', home, name="home")
]