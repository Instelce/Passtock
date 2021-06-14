from django.shortcuts import render


def home(request):
    return render(request, 'password/home.html', context={})
