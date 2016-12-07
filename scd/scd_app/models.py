# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ScdComutador(models.Model):
    comut_id = models.IntegerField(primary_key=True)
    comut_nome = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'scd_comutador'


class ScdConflito(models.Model):
    con_id = models.AutoField(primary_key=True)
    con_flow_principal = models.ForeignKey('ScdFlow', db_column='con_flow_principal', related_name='con_flow_principal')
    con_flow_analisada = models.ForeignKey('ScdFlow', db_column='con_flow_analisada', related_name='con_flow_analisada')
    con_sugestao = models.TextField(blank=True, null=True)
    con_nivel = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'scd_conflito'


class ScdFlow(models.Model):
    fl_flowtable = models.IntegerField(blank=True, null=True)
    fl_dl_dst = models.TextField(blank=True, null=True)  # This field type is a guess.
    fl_dl_src = models.TextField(blank=True, null=True)  # This field type is a guess.
    fl_nw_src = models.TextField(blank=True, null=True)  # This field type is a guess.
    fl_nw_dst = models.TextField(blank=True, null=True)  # This field type is a guess.
    fl_priority = models.IntegerField(blank=True, null=True)
    fl_idle_timeout = models.IntegerField(blank=True, null=True)
    fl_hard_timeout = models.IntegerField(blank=True, null=True)
    fl_nw_tos = models.TextField(blank=True, null=True)  # This field type is a guess.
    fl_nw_proto = models.TextField(blank=True, null=True)  # This field type is a guess.
    fl_dl_vlan = models.TextField(blank=True, null=True)  # This field type is a guess.
    fl_dl_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    fl_in_port = models.TextField(blank=True, null=True)  # This field type is a guess.
    fl_actions = models.TextField(blank=True, null=True)  # This field type is a guess.
    fl_tp_src = models.TextField(blank=True, null=True)  # This field type is a guess.
    fl_tp_dst = models.TextField(blank=True, null=True)  # This field type is a guess.
    fl_id = models.TextField(primary_key=True)
    id_comutador = models.ForeignKey(ScdComutador, db_column='id_comutador')

    def __unicode__(self):
        return self.fl_id

    class Meta:
        db_table = 'scd_flow'