# Generated by Django 4.0.6 on 2022-07-28 00:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_customer_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='name',
        ),
    ]
