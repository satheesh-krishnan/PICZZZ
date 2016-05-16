# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pic', '0005_auto_20160327_1608'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photos',
            old_name='code',
            new_name='pic_name',
        ),
    ]
