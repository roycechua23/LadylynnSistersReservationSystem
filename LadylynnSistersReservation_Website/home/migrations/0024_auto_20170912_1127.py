# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-12 03:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_userprofileinfo_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Foods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(max_length=100)),
                ('food_package', models.ManyToManyField(to='home.CateringPackages')),
            ],
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='eventtype',
            new_name='event_type',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='eventdate',
        ),
        migrations.AddField(
            model_name='reservation',
            name='event_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='event_time',
            field=models.TimeField(default='0:00'),
            preserve_default=False,
        ),
    ]
