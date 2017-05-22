# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-17 19:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myuw', '0003_rescategorylink_pce'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=512)),
                ('label', models.CharField(max_length=50, null=True)),
                ('url_key', models.SlugField(max_length=40)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='myuw.User')),
            ],
        ),
        migrations.CreateModel(
            name='HiddenLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=512)),
                ('url_key', models.SlugField(max_length=40)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='myuw.User')),
            ],
        ),
        migrations.CreateModel(
            name='PopularLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('affiliation', models.CharField(max_length=80, null=True)),
                ('pce', models.NullBooleanField()),
                ('campus', models.CharField(max_length=8, null=True)),
                ('url', models.CharField(max_length=512)),
                ('label', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='VisitedLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=512)),
                ('label', models.CharField(max_length=50, null=True)),
                ('is_anonymous', models.BooleanField(default=True)),
                ('is_student', models.BooleanField(default=False)),
                ('is_undegrad', models.BooleanField(default=False)),
                ('is_grad_student', models.BooleanField(default=False)),
                ('is_employee', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_faculty', models.BooleanField(default=False)),
                ('is_seattle', models.BooleanField(default=False)),
                ('is_tacoma', models.BooleanField(default=False)),
                ('is_bothell', models.BooleanField(default=False)),
                ('is_pce', models.BooleanField(default=False)),
                ('is_student_employee', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=20)),
                ('visit_date', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='hiddenlink',
            unique_together=set([('url_key', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='customlink',
            unique_together=set([('url_key', 'user')]),
        ),
    ]
