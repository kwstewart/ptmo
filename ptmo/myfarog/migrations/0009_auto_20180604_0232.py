# Generated by Django 2.0.5 on 2018-06-04 02:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myfarog', '0008_characterspell'),
    ]

    operations = [
        migrations.AlterField(
            model_name='characterspell',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='spells', to='myfarog.Character'),
        ),
    ]
