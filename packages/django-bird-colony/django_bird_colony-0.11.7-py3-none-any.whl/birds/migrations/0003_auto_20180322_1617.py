# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-03-22 20:17
from __future__ import unicode_literals

from django.db import migrations, models


def set_booleans(apps, schema_editor):
    Status = apps.get_model("birds", "Status")
    for status in Status.objects.all():
        status.adds = status.count > 0
        status.removes = status.count < 0
        status.save()


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0002_auto_20180130_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='adds',
            field=models.BooleanField(default=False, help_text='select for acquisition events'),
        ),
        migrations.AddField(
            model_name='status',
            name='removes',
            field=models.BooleanField(default=False, help_text='select for loss/death/removal events'),
        ),
        migrations.AlterField(
            model_name='status',
            name='count',
            field=models.SmallIntegerField(choices=[(0, '0'), (-1, '-1'), (1, '+1')], default=0, help_text='1: animal acquired; -1: animal lost/died/removed; 0: no change'),
        ),
        migrations.RunPython(set_booleans)
    ]
