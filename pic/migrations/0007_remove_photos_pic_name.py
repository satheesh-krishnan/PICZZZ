# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pic', '0006_auto_20160403_0216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photos',
            name='pic_name',
        ),
    ]
