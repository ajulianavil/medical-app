# Generated by Django 4.1.7 on 2023-04-09 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_appuser_roles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appuser',
            name='useremail',
        ),
    ]
