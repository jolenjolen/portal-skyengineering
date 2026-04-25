# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TblAudit(models.Model):
    user = models.ForeignKey('TblUser', models.DO_NOTHING, db_column='user', blank=True, null=True)
    action = models.TextField()
    datetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_audit'


class TblDepartment(models.Model):
    name = models.TextField(unique=True)
    department_head = models.ForeignKey('TblUser', models.DO_NOTHING, db_column='department_head', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_department'


class TblDependencies(models.Model):
    upstream = models.BooleanField(blank=True, null=True)
    downstream = models.BooleanField(blank=True, null=True)
    team = models.ForeignKey('TblTeam', models.DO_NOTHING, db_column='team', blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    dependency_team_name = models.TextField(blank=True,null=True)

    class Meta:
        managed = False
        db_table = 'tbl_dependencies'


class TblProject(models.Model):
    name = models.TextField()
    team = models.ForeignKey('TblTeam', models.DO_NOTHING, db_column='team', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    codebase = models.TextField(blank=True, null=True)
    jira_board = models.TextField(blank=True, null=True)
    created = models.DateTimeField()
    status = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_project'


class TblTeam(models.Model):
    name = models.TextField(unique=True)
    team_leader = models.ForeignKey('TblUser', models.DO_NOTHING, db_column='team_leader', blank=True, null=True)
    department = models.ForeignKey(TblDepartment, models.DO_NOTHING, db_column='department', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    skills_and_tech = models.TextField(blank=True, null=True)
    software_owned_and_evolved = models.TextField(blank=True, null=True)
    versioning = models.TextField(blank=True, null=True)
    agile_practices = models.TextField(blank=True, null=True)  # This field type is a guess.
    slack = models.TextField(blank=True, null=True)
    wiki = models.TextField(blank=True, null=True)
    wiki_search_terms = models.TextField(blank=True, null=True)  # This field type is a guess.
    daily_standup = models.DateTimeField(blank=True, null=True)
    active_projects = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_team'


class TblUser(models.Model):
    fname = models.TextField()
    sname = models.TextField(blank=True, null=True)
    uname = models.TextField(unique=True)
    email = models.TextField(unique=True)
    password = models.TextField()
    role = models.TextField(blank=True, null=True)
    created = models.DateTimeField()
    last_login = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()
    team = models.ForeignKey(TblTeam, models.DO_NOTHING, db_column='team', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_user'
