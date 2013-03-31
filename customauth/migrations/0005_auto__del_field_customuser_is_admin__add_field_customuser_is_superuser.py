# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'CustomUser.is_admin'
        db.delete_column(u'customauth_customuser', 'is_admin')

        # Adding field 'CustomUser.is_superuser'
        db.add_column(u'customauth_customuser', 'is_superuser',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CustomUser.year_of_birth'
        db.add_column(u'customauth_customuser', 'year_of_birth',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1992),
                      keep_default=False)

        # Adding field 'CustomUser.gender'
        db.add_column(u'customauth_customuser', 'gender',
                      self.gf('django.db.models.fields.CharField')(default='M', max_length=1),
                      keep_default=False)

        # Adding M2M table for field groups on 'CustomUser'
        db.create_table(u'customauth_customuser_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customuser', models.ForeignKey(orm[u'customauth.customuser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(u'customauth_customuser_groups', ['customuser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'CustomUser'
        db.create_table(u'customauth_customuser_user_permissions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customuser', models.ForeignKey(orm[u'customauth.customuser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(u'customauth_customuser_user_permissions', ['customuser_id', 'permission_id'])


    def backwards(self, orm):
        # Adding field 'CustomUser.is_admin'
        db.add_column(u'customauth_customuser', 'is_admin',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'CustomUser.is_superuser'
        db.delete_column(u'customauth_customuser', 'is_superuser')

        # Deleting field 'CustomUser.year_of_birth'
        db.delete_column(u'customauth_customuser', 'year_of_birth')

        # Deleting field 'CustomUser.gender'
        db.delete_column(u'customauth_customuser', 'gender')

        # Removing M2M table for field groups on 'CustomUser'
        db.delete_table('customauth_customuser_groups')

        # Removing M2M table for field user_permissions on 'CustomUser'
        db.delete_table('customauth_customuser_user_permissions')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'customauth.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'items_used': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['items.Item']", 'through': u"orm['items.ItemUsageExperience']", 'symmetrical': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'year_of_birth': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'items.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'items.item': {
            'Meta': {'object_name': 'Item'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.Category']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customauth.CustomUser']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'items.itemusageduration': {
            'Meta': {'unique_together': "(('string', 'value'),)", 'object_name': 'ItemUsageDuration'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'string': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'items.itemusageexperience': {
            'Meta': {'object_name': 'ItemUsageExperience'},
            'date_verified': ('django.db.models.fields.DateTimeField', [], {}),
            'duration': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['items.ItemUsageDuration']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.Item']"}),
            'rating': ('django.db.models.fields.related.ForeignKey', [], {'default': '4', 'to': u"orm['items.ItemUsageRating']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customauth.CustomUser']"})
        },
        u'items.itemusagerating': {
            'Meta': {'unique_together': "(('string', 'value'),)", 'object_name': 'ItemUsageRating'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'string': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'value': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['customauth']