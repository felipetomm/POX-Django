# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scd_app', '0005_scdregraconflito'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scdregraconflito',
            name='id_conflito',
        ),
        migrations.RemoveField(
            model_name='scdregraconflito',
            name='id_regra',
        ),
        migrations.DeleteModel(
            name='ScdRegraConflito',
        ),
    ]
