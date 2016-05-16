# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pic', '0007_remove_photos_pic_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfollows',
            name='from_user',
            field=models.CharField(max_length=128),
        ),
    ]
