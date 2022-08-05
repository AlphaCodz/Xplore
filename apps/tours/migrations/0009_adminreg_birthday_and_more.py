# Generated by Django 4.0.6 on 2022-08-05 19:25

import birthday.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0008_remove_adminreg_birthday_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminreg',
            name='birthday',
            field=birthday.fields.BirthdayField(null=True),
        ),
        migrations.AddField(
            model_name='adminreg',
            name='birthday_dayofyear_internal',
            field=models.PositiveSmallIntegerField(default=None, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='approved_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='tours.adminreg'),
        ),
    ]
