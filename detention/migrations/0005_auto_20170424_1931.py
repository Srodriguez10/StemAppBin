# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-25 00:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detention', '0004_detention_demerit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='grade_level',
            field=models.CharField(choices=[('09', '09'), ('10', '10'), ('11', '11'), ('12', '12')], max_length=2),
        ),
    ]
