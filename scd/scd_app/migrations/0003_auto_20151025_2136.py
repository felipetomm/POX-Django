# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scd_app', '0002_auto_20151025_2057'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ScdComutador',
        ),
        migrations.DeleteModel(
            name='ScdConflito',
        ),
        migrations.DeleteModel(
            name='ScdFlow',
        ),
    ]
