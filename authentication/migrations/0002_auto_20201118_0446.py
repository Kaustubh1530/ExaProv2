# Generated by Django 3.0.7 on 2020-11-18 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='register',
            name='id',
        ),
        migrations.AlterField(
            model_name='register',
            name='email',
            field=models.EmailField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
