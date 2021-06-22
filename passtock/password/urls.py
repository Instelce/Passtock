from django.urls import path
from .views import *

handler404 = 'password.views.handler404'
handler500 = 'password.views.handler500'

app_name = 'password'
urlpatterns = [
    path('<str:username>/dashboard/', Dashboard.as_view(extra_context={'title': 'Dashboard'}), name="dashboard"),
    path('<str:username>/password/<int:pk>/', PasswordDetailView.as_view(extra_context={'title': 'Detail'}), name="detail"),
    path('create/', PasswordCreateView.as_view(extra_context={'title': 'Create'}), name="create"),
    path('<str:username>/password/update/<int:pk>/', PasswordUpdateView.as_view(extra_context={'title': 'Update'}), name="update"),
    path('<str:username>/password/delete/<int:pk>/', PasswordDeleteView.as_view(extra_context={'title': 'Delete'}), name="delete"),
    path('privacy-policy/', privacy_policy, name="privacy-policy"),
    path('', home, name="home")
]