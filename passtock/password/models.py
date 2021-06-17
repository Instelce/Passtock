from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Password(models.Model):
    site_name = models.CharField(max_length=40)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')

    def __str__(self):
        return f'{self.site_name} Password - {self.owner}'

    def get_absolute_url(self):
        return reverse('password:detail', kwargs={'pk': self.pk, 'username': self.owner})
