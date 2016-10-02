# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-01 19:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lbattachment', '0002_auto_20161002_0335'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('descn', models.TextField(blank=True)),
                ('oid', models.PositiveIntegerField(default=999)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ('-oid', 'created_on'),
            },
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=110)),
                ('description', models.TextField(default='')),
                ('oid', models.PositiveIntegerField(default=999)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(blank=True, null=True)),
                ('num_topics', models.IntegerField(default=0)),
                ('num_posts', models.IntegerField(default=0)),
                ('admins', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lbforum.Category')),
            ],
            options={
                'verbose_name': 'Forum',
                'verbose_name_plural': 'Forums',
                'permissions': (('sft_mgr_forum', 'Forum-Administrator'),),
                'ordering': ('oid', '-created_on'),
            },
        ),
        migrations.CreateModel(
            name='LBForumUserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(default='', max_length=255, verbose_name='Nickname')),
                ('avatar', easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='imgs/avatars', verbose_name='Avatar')),
                ('bio', models.TextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='lbforum_profile', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poster_ip', models.GenericIPAddressField()),
                ('topic_post', models.BooleanField(default=False)),
                ('format', models.CharField(choices=[('bbcode', 'BBCode'), ('markdown', 'Markdown'), ('html', 'Html')], default='bbcode', max_length=20)),
                ('message', models.TextField()),
                ('has_imgs', models.BooleanField(default=False)),
                ('has_attachments', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(blank=True, null=True)),
                ('attachments', models.ManyToManyField(blank=True, to='lbattachment.LBAttachment')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_updated_by_posts', to=settings.AUTH_USER_MODEL)),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ('-created_on',),
                'get_latest_by': ('created_on',),
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=999)),
                ('num_views', models.IntegerField(default=0)),
                ('num_replies', models.PositiveSmallIntegerField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(blank=True, null=True)),
                ('last_reply_on', models.DateTimeField(auto_now_add=True)),
                ('has_imgs', models.BooleanField(default=False)),
                ('has_attachments', models.BooleanField(default=False)),
                ('need_replay', models.BooleanField(default=False)),
                ('need_reply_attachments', models.BooleanField(default=False)),
                ('closed', models.BooleanField(default=False)),
                ('sticky', models.BooleanField(default=False)),
                ('hidden', models.BooleanField(default=False)),
                ('level', models.SmallIntegerField(choices=[(30, 'Default'), (60, 'Distillate')], default=30)),
                ('forum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lbforum.Forum', verbose_name='Forum')),
                ('last_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_post_topics', to='lbforum.Post', verbose_name='Last post')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='lbforum.Post', verbose_name='Post')),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
                'ordering': ('-last_reply_on',),
                'get_latest_by': 'created_on',
            },
        ),
        migrations.CreateModel(
            name='TopicType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('forum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lbforum.Forum', verbose_name='Forum')),
            ],
        ),
        migrations.AddField(
            model_name='topic',
            name='topic_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lbforum.TopicType', verbose_name='Topic Type'),
        ),
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='lbforum.Topic', verbose_name='Topic'),
        ),
        migrations.AddField(
            model_name='forum',
            name='last_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lbforum.Post', verbose_name='Last post'),
        ),
    ]
