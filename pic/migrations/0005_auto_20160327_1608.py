# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pic', '0004_auto_20160319_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='photos',
            name='code',
            field=models.CharField(default='m', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='photos',
            name='upload_photo',
            field=models.ImageField(upload_to=b'photo', blank=True),
        ),
    ]
