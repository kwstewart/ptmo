# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-27 04:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ptmo', '0011_roomitem_force_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'UserPreference',
                'verbose_name_plural': 'UserPreferences',
            },
        ),
        migrations.AddField(
            model_name='level',
            name='slack_channel',
            field=models.CharField(default='#', max_length=16),
            preserve_default=False,
        ),
    ]
