# Generated by Django 2.0.5 on 2018-06-03 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myfarog', '0006_inventoryslot_character'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryslot',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='inventory_slots', to='myfarog.Character'),
        ),
    ]