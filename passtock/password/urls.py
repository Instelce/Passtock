from django.urls import path
from .views import *

app_name = 'password'
urlpatterns = [
    path('<str:username>/dashboard/', Dashboard.as_view(), name="dashboard"),
    path('<str:username>/password/<int:pk>/', PasswordDetailView.as_view(), name="detail"),
    path('create/', PasswordCreateView.as_view(), name="create"),
    path('', home, name="home")
]