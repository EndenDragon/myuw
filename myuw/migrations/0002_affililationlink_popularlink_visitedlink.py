# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-26 22:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myuw', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AffililationLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
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
            ],
        ),
        migrations.CreateModel(
            name='PopularLink',
            fields=[
                ('affililationlink_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='myuw.AffililationLink')),
            ],
            bases=('myuw.affililationlink',),
        ),
        migrations.CreateModel(
            name='VisitedLink',
            fields=[
                ('affililationlink_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='myuw.AffililationLink')),
                ('username', models.CharField(max_length=20)),
                ('visit_date', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            bases=('myuw.affililationlink',),
        ),
    ]