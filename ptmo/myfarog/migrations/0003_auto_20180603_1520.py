# Generated by Django 2.0.5 on 2018-06-03 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myfarog', '0002_auto_20180603_0158'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='pants_equipment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myfarog.Pants'),
        ),
        migrations.AddField(
            model_name='character',
            name='shirt_equipment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myfarog.Shirt'),
        ),
    ]
