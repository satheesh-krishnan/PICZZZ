# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pic', '0003_auto_20160117_1523'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photos',
            old_name='photo_name',
            new_name='upload_photo',
        ),
    ]
