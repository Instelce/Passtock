# Generated by Django 3.2.4 on 2021-06-18 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('password', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='password',
            name='image_url',
            field=models.ImageField(blank=True, upload_to='image_site'),
        ),
    ]
