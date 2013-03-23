# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ItemUsageRating'
        db.create_table(u'items_itemusagerating', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('string', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('value', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'items', ['ItemUsageRating'])

        # Adding model 'ItemUsageDuration'
        db.create_table(u'items_itemusageduration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('string', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'items', ['ItemUsageDuration'])


        # Renaming column for 'ItemUsageExperience.duration' to match new field type.
        db.rename_column(u'items_itemusageexperience', 'duration', 'duration_id')
        # Changing field 'ItemUsageExperience.duration'
        db.alter_column(u'items_itemusageexperience', 'duration_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.ItemUsageDuration']))
        # Adding index on 'ItemUsageExperience', fields ['duration']
        db.create_index(u'items_itemusageexperience', ['duration_id'])


        # Renaming column for 'ItemUsageExperience.rating' to match new field type.
        db.rename_column(u'items_itemusageexperience', 'rating', 'rating_id')
        # Changing field 'ItemUsageExperience.rating'
        db.alter_column(u'items_itemusageexperience', 'rating_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.ItemUsageRating']))
        # Adding index on 'ItemUsageExperience', fields ['rating']
        db.create_index(u'items_itemusageexperience', ['rating_id'])


    def backwards(self, orm):
        # Removing index on 'ItemUsageExperience', fields ['rating']
        db.delete_index(u'items_itemusageexperience', ['rating_id'])

        # Removing index on 'ItemUsageExperience', fields ['duration']
        db.delete_index(u'items_itemusageexperience', ['duration_id'])

        # Deleting model 'ItemUsageRating'
        db.delete_table(u'items_itemusagerating')

        # Deleting model 'ItemUsageDuration'
        db.delete_table(u'items_itemusageduration')


        # Renaming column for 'ItemUsageExperience.duration' to match new field type.
        db.rename_column(u'items_itemusageexperience', 'duration_id', 'duration')
        # Changing field 'ItemUsageExperience.duration'
        db.alter_column(u'items_itemusageexperience', 'duration', self.gf('django.db.models.fields.PositiveSmallIntegerField')())

        # Renaming column for 'ItemUsageExperience.rating' to match new field type.
        db.rename_column(u'items_itemusageexperience', 'rating_id', 'rating')
        # Changing field 'ItemUsageExperience.rating'
        db.alter_column(u'items_itemusageexperience', 'rating', self.gf('django.db.models.fields.PositiveSmallIntegerField')())

    models = {
        u'customauth.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'items_used': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['items.Item']", 'through': u"orm['items.ItemUsageExperience']", 'symmetrical': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
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
            'Meta': {'object_name': 'ItemUsageDuration'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'string': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'items.itemusageexperience': {
            'Meta': {'object_name': 'ItemUsageExperience'},
            'duration': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.ItemUsageDuration']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.Item']"}),
            'rating': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.ItemUsageRating']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customauth.CustomUser']"})
        },
        u'items.itemusagerating': {
            'Meta': {'object_name': 'ItemUsageRating'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'string': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'value': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['items']