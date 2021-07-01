from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.forms.models import model_to_dict
from django.template import RequestContext
from django.template.loader import get_template
from django.conf import settings
from xhtml2pdf import pisa
from io import BytesIO
from .models import Password
from .helpers import *
import json
import uuid


def save_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def home(request):
    return render(request, 'password/home.html')


def generator(request):
    return render(request, 'password/generator.html', {'title': 'Generator'})


def privacy_policy(request):
    return render(request, 'password/privacy_policy.html', {'title': 'Privacy Policy'})


def handler404(request, exception):
    return render(request, 'password/404.html', RequestContext(request))


def handler500(request):
    return render(request, 'password/500.html', RequestContext(request))


class ViewPDF(View):
    def get(self, request, username):
        data = {
            'passwords': Password.objects.filter(owner=self.request.user).order_by('site_name'),
            'user': self.request.user
        }
        pdf = save_pdf("password/pdf.html", data)
        return HttpResponse(pdf, content_type='application/pdf')


class Dashboard(LoginRequiredMixin, ListView):
    model = Password
    template_name = 'password/dashboard.html'
    context_object_name = 'passwords'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pass_json"] = json.dumps(list(Password.objects.filter(owner=self.request.user).values()))
        return context

    def get_queryset(self):
        return Password.objects.filter(owner=self.request.user).order_by('site_name')


class PasswordDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Password
    extra_context = {'title': 'Detail'}

    def test_func(self):
        password = self.get_object()
        if self.request.user == password.owner:
            return True
        return False


class PasswordCreateView(LoginRequiredMixin, CreateView):
    model = Password
    template_name = 'password/password_create_form.html'
    fields = ['site_name', 'password', 'email', 'image_url']
    extra_context = {'title': 'Create'}

    def get_success_url(self):
        owner = self.request.user
        messages.success(self.request, f'{self.object.site_name} password has been created')
        return reverse_lazy('password:dashboard', kwargs={'username': owner})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        # form.instance.email = self.request.user.email
        return super(PasswordCreateView, self).form_valid(form)


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
