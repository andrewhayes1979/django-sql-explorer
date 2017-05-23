# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0006_query_connection'),
    ]

    operations = [
        migrations.AddField(
            model_name='querylog',
            name='connection',
            field=models.CharField(default=b'default', max_length=255),
        ),
    ]
