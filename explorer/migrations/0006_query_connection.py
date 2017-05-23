# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0005_auto_20160105_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='connection',
            field=models.CharField(default=b'default', help_text=b'Named database connection defined in Django settings to run SQL against', max_length=255),
        ),
    ]
