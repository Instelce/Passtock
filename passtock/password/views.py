from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Password


def home(request):
    return render(request, 'password/home.html', context={})


class Dashboard(LoginRequiredMixin, ListView):
    model = Password
    template_name = 'password/dashboard.html'
    context_object_name = 'passwords'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Password.objects.filter(owner=user).order_by('site_name')


class PasswordDetailView(DetailView):
    model = Password


class PasswordCreateView(CreateView):
    model = Password
    fields = ['site_name', 'email', 'password']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
