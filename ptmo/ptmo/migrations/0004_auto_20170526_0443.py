# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-26 04:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ptmo', '0003_auto_20170526_0424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='door',
            name='inspect_text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='item',
            name='inspect_text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='level',
            name='text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='room',
            name='text',
            field=models.TextField(),
        ),
    ]