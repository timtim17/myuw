# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-02 19:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myuw', '0007_new_visitedlink'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCourseDisplay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveSmallIntegerField()),
                ('quarter', models.CharField(max_length=10)),
                ('section_label', models.CharField(max_length=64)),
                ('color_id', models.PositiveSmallIntegerField()),
                ('pin_on_teaching_page', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='myuw.User')),
            ],
            options={
                'ordering': ['section_label'],
                'db_table': 'user_course_display_pref',
            },
        ),
        migrations.AlterUniqueTogether(
            name='usercoursedisplay',
            unique_together=set([('user', 'section_label')]),
        ),
        migrations.AlterIndexTogether(
            name='usercoursedisplay',
            index_together=set([('user', 'section_label'), ('user', 'year', 'quarter')]),
        ),
    ]
