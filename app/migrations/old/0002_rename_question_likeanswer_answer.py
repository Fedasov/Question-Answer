# Generated by Django 4.2.6 on 2023-11-15 00:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likeanswer',
            old_name='question',
            new_name='answer',
        ),
    ]