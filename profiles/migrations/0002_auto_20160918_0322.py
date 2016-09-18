# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(default='none', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Teamroom',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('content', models.CharField(max_length=50)),
                ('date_time', models.DateTimeField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'permissions': (('can_create_team_profile', 'Can create team profile'), ('can_edit_team_profile', 'Can edit team profile'))},
        ),
        migrations.RemoveField(
            model_name='team',
            name='need',
        ),
        migrations.AddField(
            model_name='student',
            name='applied',
            field=models.ManyToManyField(to='profiles.Team', blank=True, related_name='applier'),
        ),
        migrations.AddField(
            model_name='team',
            name='content',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='talent',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='team',
            name='interest',
            field=models.ForeignKey(to='profiles.Interest', default=1),
        ),
        migrations.DeleteModel(
            name='Talent',
        ),
        migrations.AddField(
            model_name='teamroom',
            name='speaker',
            field=models.ForeignKey(to='profiles.Student', null=True),
        ),
        migrations.AddField(
            model_name='teamroom',
            name='team',
            field=models.ForeignKey(to='profiles.Team', null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='role',
            field=models.ForeignKey(to='profiles.Role', default=1),
        ),
    ]
