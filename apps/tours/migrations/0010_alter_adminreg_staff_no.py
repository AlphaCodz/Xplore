# Generated by Django 4.0.6 on 2022-08-05 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0009_adminreg_birthday_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminreg',
            name='staff_no',
            field=models.CharField(max_length=6),
        ),
    ]
