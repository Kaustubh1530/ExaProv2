# Generated by Django 3.0.7 on 2020-11-17 15:03

import datetime
from django.db import migrations, models
from django.utils.timezone import localtime
from django.utils import timezone

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('message', models.TextField(max_length=500)),
                ('time', models.DateTimeField(default=localtime)),
            ],
        ),
    ]
