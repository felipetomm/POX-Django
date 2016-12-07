# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scd_app', '0004_auto_20151025_2140'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScdRegraConflito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_conflito', models.ForeignKey(to='scd_app.ScdConflito')),
                ('id_regra', models.ForeignKey(to='scd_app.ScdFlow')),
            ],
        ),
    ]
