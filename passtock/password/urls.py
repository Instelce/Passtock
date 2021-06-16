from django.urls import path
from .views import *

app_name = 'password'
urlpatterns = [
    path('dashboard/', dashboard, name="dashboard"),
    path('', home, name="home")
]