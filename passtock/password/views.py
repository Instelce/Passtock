from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.forms.models import model_to_dict
from .models import Password
import json


def home(request):
    return render(request, 'password/home.html')


class Dashboard(LoginRequiredMixin, ListView):
    model = Password
    template_name = 'password/dashboard.html'
    context_object_name = 'passwords'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pass_json"] = json.dumps(list(Password.objects.filter(owner=self.request.user).values()))
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Password.objects.filter(owner=user).order_by('site_name')


class PasswordDetailView(LoginRequiredMixin, DetailView):
    model = Password
    extra_context = {'title': 'Detail'}


class PasswordCreateView(LoginRequiredMixin, CreateView):
    model = Password
    template_name = 'password/password_create_form.html'
    fields = ['site_name', 'email', 'password', 'image_url']
    extra_context = {'title': 'Create'}

    def get_success_url(self):
        owner = self.request.user
        messages.success(self.request, f'{self.object.site_name} password has been created')
        return reverse_lazy('password:dashboard', kwargs={'username': owner})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PasswordUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Password
    template_name = 'password/password_update_form.html'
    fields = ['site_name', 'email', 'password', 'image_url']
    extra_context = {'title': 'Update'}

    def get_success_url(self):
        owner = self.request.user
        messages.success(self.request, f'{self.object.site_name} password has been updated')
        return reverse_lazy('password:dashboard', kwargs={'username': owner})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        password = self.get_object()
        if self.request.user == password.owner:
            return True
        return False


class PasswordDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Password
    extra_context = {'title': 'Delete'}

    def get_success_url(self):
        owner = self.request.user
        messages.success(self.request, f'{self.object.site_name} password has been deleted')
        return reverse_lazy('password:dashboard', kwargs={'username': owner})

    def test_func(self):
        password = self.get_object()
        if self.request.user == password.owner:
            return True
        return False
