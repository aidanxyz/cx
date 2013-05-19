# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Item.reviewers_count'
        db.add_column(u'items_item', 'reviewers_count',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Item.reviewers_count'
        db.delete_column(u'items_item', 'reviewers_count')


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
            'avg_rating': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '3', 'decimal_places': '2'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.Category']"}),
            'cons_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'cover_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cover_image'", 'null': 'True', 'to': u"orm['items.ItemImage']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customauth.CustomUser']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latest_feedback': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'items_latest_set'", 'null': 'True', 'to': u"orm['reviews.Feedback']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'possible_duplicates': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['items.ItemPossibleDuplicates']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'pros_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'reviewers_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'specifications': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['items.Specification']", 'symmetrical': 'False'}),
            'views_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'items.itemapprovalhistory': {
            'Meta': {'object_name': 'ItemApprovalHistory'},
            'date_approved': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.Item']"}),
            'moderator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customauth.CustomUser']"})
        },
        u'items.itemdeactivationhistory': {
            'Meta': {'object_name': 'ItemDeactivationHistory'},
            'date_deactivated': ('django.db.models.fields.DateTimeField', [], {}),
            'duplicate_of': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'duplicate_of'", 'null': 'True', 'to': u"orm['items.Item']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.Item']"}),
            'moderator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customauth.CustomUser']"}),
            'reason': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.ItemDeactivationReason']"})
        },
        u'items.itemdeactivationreason': {
            'Meta': {'object_name': 'ItemDeactivationReason'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'items.itemedithistory': {
            'Meta': {'object_name': 'ItemEditHistory'},
            'date_edited': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.Item']"}),
            'moderator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customauth.CustomUser']"}),
            'old_value': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'other_reason': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'reason': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.ItemEditReason']"})
        },
        u'items.itemeditreason': {
            'Meta': {'object_name': 'ItemEditReason'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'items.itemimage': {
            'Meta': {'unique_together': "(('image', 'image'),)", 'object_name': 'ItemImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'image_gallery_thumb': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.Item']"})
        },
        u'items.itempossibleduplicates': {
            'Meta': {'object_name': 'ItemPossibleDuplicates'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'str_list': ('django.db.models.fields.CharField', [], {'max_length': '512'})
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
            'Meta': {'ordering': "('value',)", 'unique_together': "(('string', 'value'),)", 'object_name': 'ItemUsageRatingType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'string': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'value': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'items.price': {
            'Meta': {'object_name': 'Price'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        u'items.specification': {
            'Meta': {'unique_together': "(('name', 'spectype'),)", 'object_name': 'Specification'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'spectype': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.SpecificationType']"})
        },
        u'items.specificationtype': {
            'Meta': {'object_name': 'SpecificationType'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['items.Category']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'reviews.feedback': {
            'Meta': {'ordering': "('-score', 'date_created')", 'unique_together': "(('body', 'item', 'is_positive'),)", 'object_name': 'Feedback'},
            'agrees_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'body': ('django.db.models.fields.CharField', [], {'max_length': '144'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customauth.CustomUser']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'details_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'disagrees_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_positive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.Item']"}),
            'priority_1_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'priority_2_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'priority_3_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['items']