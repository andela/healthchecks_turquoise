# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-06 20:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_check_n_nags'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='nag_enabled',
            field=models.BooleanField(default=True),
        ),
    ]
