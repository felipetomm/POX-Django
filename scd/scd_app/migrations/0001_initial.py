# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScdComutador',
            fields=[
                ('comut_id', models.AutoField(serialize=False, primary_key=True)),
                ('comut_nome', models.CharField(max_length=45, null=True, blank=True)),
            ],
            options={
                'db_table': 'scd_comutador',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ScdConflito',
            fields=[
                ('con_id', models.AutoField(serialize=False, primary_key=True)),
                ('con_conflito', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'scd_conflito',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ScdFlow',
            fields=[
                ('fl_id', models.AutoField(serialize=False, primary_key=True)),
                ('id_flowtable', models.IntegerField(null=True, blank=True)),
                ('fl_dl_dst', models.CharField(max_length=17, null=True, blank=True)),
                ('fl_dl_src', models.CharField(max_length=17, null=True, blank=True)),
                ('fl_nw_src', models.CharField(max_length=15, null=True, blank=True)),
                ('fl_nw_dst', models.CharField(max_length=15, null=True, blank=True)),
                ('fl_priority', models.IntegerField(null=True, blank=True)),
                ('fl_nw_tos', models.TextField(null=True, blank=True)),
                ('fl_nw_proto', models.TextField(null=True, blank=True)),
                ('fl_dl_vlan', models.TextField(null=True, blank=True)),
                ('fl_dl_type', models.TextField(null=True, blank=True)),
                ('fl_idle_timeout', models.IntegerField(null=True, blank=True)),
                ('fl_hard_timeout', models.IntegerField(null=True, blank=True)),
                ('fl_in_port', models.TextField(null=True, blank=True)),
                ('fl_actions', models.TextField(null=True, blank=True)),
                ('fl_tp_src', models.TextField(null=True, blank=True)),
                ('fl_tp_dst', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'scd_flow',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ScdFlowtable',
            fields=[
                ('ft_id', models.AutoField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'scd_flowtable',
                'managed': False,
            },
        ),
    ]
