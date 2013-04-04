# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'ItemUsageDuration', fields ['string', 'value']
        db.delete_unique(u'items_itemusageduration', ['string', 'value'])

        # Removing unique constraint on 'ItemUsageRating', fields ['string', 'value']
        db.delete_unique(u'items_itemusagerating', ['string', 'value'])

        # Deleting model 'ItemUsageRating'
        db.delete_table(u'items_itemusagerating')

        # Deleting model 'ItemUsageDuration'
        db.delete_table(u'items_itemusageduration')

        # Adding model 'ItemUsageDurationType'
        db.create_table(u'items_itemusagedurationtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('string', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'items', ['ItemUsageDurationType'])

        # Adding unique constraint on 'ItemUsageDurationType', fields ['string', 'value']
        db.create_unique(u'items_itemusagedurationtype', ['string', 'value'])

        # Adding model 'ItemUsageRatingType'
        db.create_table(u'items_itemusageratingtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('string', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('value', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'items', ['ItemUsageRatingType'])

        # Adding unique constraint on 'ItemUsageRatingType', fields ['string', 'value']
        db.create_unique(u'items_itemusageratingtype', ['string', 'value'])


        # Changing field 'ItemUsageExperience.rating'
        db.alter_column(u'items_itemusageexperience', 'rating_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.ItemUsageRatingType']))

        # Changing field 'ItemUsageExperience.duration'
        db.alter_column(u'items_itemusageexperience', 'duration_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.ItemUsageDurationType']))

    def backwards(self, orm):
        # Removing unique constraint on 'ItemUsageRatingType', fields ['string', 'value']
        db.delete_unique(u'items_itemusageratingtype', ['string', 'value'])

        # Removing unique constraint on 'ItemUsageDurationType', fields ['string', 'value']
        db.delete_unique(u'items_itemusagedurationtype', ['string', 'value'])

        # Adding model 'ItemUsageRating'
        db.create_table(u'items_itemusagerating', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('string', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'items', ['ItemUsageRating'])

        # Adding unique constraint on 'ItemUsageRating', fields ['string', 'value']
        db.create_unique(u'items_itemusagerating', ['string', 'value'])

        # Adding model 'ItemUsageDuration'
        db.create_table(u'items_itemusageduration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('string', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'items', ['ItemUsageDuration'])

        # Adding unique constraint on 'ItemUsageDuration', fields ['string', 'value']
        db.create_unique(u'items_itemusageduration', ['string', 'value'])

        # Deleting model 'ItemUsageDurationType'
        db.delete_table(u'items_itemusagedurationtype')

        # Deleting model 'ItemUsageRatingType'
        db.delete_table(u'items_itemusageratingtype')


        # Changing field 'ItemUsageExperience.rating'
        db.alter_column(u'items_itemusageexperience', 'rating_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.ItemUsageRating']))

        # Changing field 'ItemUsageExperience.duration'
        db.alter_column(u'items_itemusageexperience', 'duration_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.ItemUsageDuration']))

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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'NC'", 'max_length': '2'})
        },
        u'items.itemusagedurationtype': {
            'Meta': {'unique_together': "(('string', 'value'),)", 'object_name': 'ItemUsageDurationType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'string': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'items.itemusageexperience': {
            'Meta': {'object_name': 'ItemUsageExperience'},
            'date_verified': ('django.db.models.fields.DateTimeField', [], {}),
            'duration': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['items.ItemUsageDurationType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.Item']"}),
            'rating': ('django.db.models.fields.related.ForeignKey', [], {'default': '4', 'to': u"orm['items.ItemUsageRatingType']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customauth.CustomUser']"})
        },
        u'items.itemusageratingtype': {
            'Meta': {'unique_together': "(('string', 'value'),)", 'object_name': 'ItemUsageRatingType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'string': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'value': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['items']