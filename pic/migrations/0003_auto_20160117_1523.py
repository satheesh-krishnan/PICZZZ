# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pic', '0002_auto_20160117_1500'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='profile_pic',
            new_name='profile_picture',
        ),
    ]
