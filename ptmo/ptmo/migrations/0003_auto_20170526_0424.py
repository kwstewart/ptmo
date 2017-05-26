# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-26 04:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

def create_level(apps, schema_editor):
    Level = apps.get_model("level","Level")
    level_1 = Level(id=0, name="tutorial", text="The tutorial level.")
    level_1.save()

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ptmo', '0002_auto_20170526_0214'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Inventory',
                'verbose_name_plural': 'Inventory',
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('text', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Level',
                'verbose_name_plural': 'Levels',
            },
        ),
        migrations.RunPython(create_level),
        migrations.CreateModel(
            name='RoomItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'RoomItem',
                'verbose_name_plural': 'RoomItems',
            },
        ),
        migrations.RenameField(
            model_name='door',
            old_name='text',
            new_name='button_text',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='text',
            new_name='button_text',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='curr_room',
            new_name='room',
        ),
        migrations.AddField(
            model_name='door',
            name='attempted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='door',
            name='inspect_text',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='attempted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='item',
            name='inspect_text',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='inspected',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=16),
        ),
        migrations.AddField(
            model_name='roomitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ptmo.Item'),
        ),
        migrations.AddField(
            model_name='roomitem',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ptmo.Room'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ptmo.Item'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='location',
            name='level',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='ptmo.Level'),
            preserve_default=False,
        ),
    ]
