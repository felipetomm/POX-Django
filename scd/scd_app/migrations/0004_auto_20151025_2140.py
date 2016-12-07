# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scd_app', '0003_auto_20151025_2136'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScdComutador',
            fields=[
                ('comut_id', models.IntegerField(serialize=False, primary_key=True)),
                ('comut_nome', models.CharField(max_length=45, null=True, blank=True)),
            ],
            options={
                'db_table': 'scd_comutador',
            },
        ),
        migrations.CreateModel(
            name='ScdConflito',
            fields=[
                ('con_id', models.AutoField(serialize=False, primary_key=True)),
                ('con_sugestao', models.TextField(null=True, blank=True)),
                ('con_nivel', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'scd_conflito',
            },
        ),
        migrations.CreateModel(
            name='ScdFlow',
            fields=[
                ('fl_flowtable', models.IntegerField(null=True, blank=True)),
                ('fl_dl_dst', models.TextField(null=True, blank=True)),
                ('fl_dl_src', models.TextField(null=True, blank=True)),
                ('fl_nw_src', models.TextField(null=True, blank=True)),
                ('fl_nw_dst', models.TextField(null=True, blank=True)),
                ('fl_priority', models.IntegerField(null=True, blank=True)),
                ('fl_idle_timeout', models.IntegerField(null=True, blank=True)),
                ('fl_hard_timeout', models.IntegerField(null=True, blank=True)),
                ('fl_nw_tos', models.TextField(null=True, blank=True)),
                ('fl_nw_proto', models.TextField(null=True, blank=True)),
                ('fl_dl_vlan', models.TextField(null=True, blank=True)),
                ('fl_dl_type', models.TextField(null=True, blank=True)),
                ('fl_in_port', models.TextField(null=True, blank=True)),
                ('fl_actions', models.TextField(null=True, blank=True)),
                ('fl_tp_src', models.TextField(null=True, blank=True)),
                ('fl_tp_dst', models.TextField(null=True, blank=True)),
                ('fl_id', models.TextField(serialize=False, primary_key=True)),
                ('id_comutador', models.ForeignKey(to='scd_app.ScdComutador', db_column='id_comutador')),
            ],
            options={
                'db_table': 'scd_flow',
            },
        ),
        migrations.AddField(
            model_name='scdconflito',
            name='con_flow_analisada',
            field=models.ForeignKey(related_name='con_flow_analisada', db_column='con_flow_analisada', to='scd_app.ScdFlow'),
        ),
        migrations.AddField(
            model_name='scdconflito',
            name='con_flow_principal',
            field=models.ForeignKey(related_name='con_flow_principal', db_column='con_flow_principal', to='scd_app.ScdFlow'),
        ),
    ]
