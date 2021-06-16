from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'password/home.html', context={})


@login_required
def dashboard(request):
    return render(request, 'password/dashboard.html', context={'title': 'Dashboard'})
