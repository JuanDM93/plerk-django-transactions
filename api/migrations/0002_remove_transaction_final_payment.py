# Generated by Django 4.0.1 on 2022-01-29 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='final_payment',
        ),
    ]
