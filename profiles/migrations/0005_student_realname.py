# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20160820_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='realname',
            field=models.CharField(default=b'', max_length=50),
            preserve_default=True,
        ),
    ]
