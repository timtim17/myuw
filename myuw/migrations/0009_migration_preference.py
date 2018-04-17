# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-10 17:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myuw', '0008_user_course_display'),
    ]

    operations = [
        migrations.CreateModel(
            name='MigrationPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_onboard_message', models.BooleanField(default=True)),
                ('display_pop_up', models.BooleanField(default=True)),
                ('use_legacy_site', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'migration_preference',
            },
        ),
        migrations.DeleteModel(
            name='CourseColor',
        ),
        migrations.DeleteModel(
            name='StudentAccountsBalances',
        ),
        migrations.RemoveField(
            model_name='user',
            name='uwregid',
        ),
        migrations.AlterField(
            model_name='user',
            name='last_visit',
            field=models.DateTimeField(),
        ),
        migrations.AddField(
            model_name='migrationpreference',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myuw.User'),
        ),
    ]
