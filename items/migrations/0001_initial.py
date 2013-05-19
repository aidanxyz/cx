# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'items_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'items', ['Category'])

        # Adding model 'Item'
        db.create_table(u'items_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')()),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customauth.CustomUser'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.Category'])),
            ('cover_image', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='cover_image', null=True, to=orm['items.ItemImage'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('latest_feedback', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='items_latest_set', null=True, to=orm['reviews.Feedback'])),
            ('views_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('pros_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('cons_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('possible_duplicates', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
        ))
        db.send_create_signal(u'items', ['Item'])

        # Adding model 'ItemApprovalHistory'
        db.create_table(u'items_itemapprovalhistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.Item'])),
            ('moderator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customauth.CustomUser'])),
            ('date_approved', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'items', ['ItemApprovalHistory'])

        # Adding model 'ItemDeactivationReason'
        db.create_table(u'items_itemdeactivationreason', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reason', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'items', ['ItemDeactivationReason'])

        # Adding model 'ItemDeactivationHistory'
        db.create_table(u'items_itemdeactivationhistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.Item'])),
            ('moderator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customauth.CustomUser'])),
            ('date_deactivated', self.gf('django.db.models.fields.DateTimeField')()),
            ('reason', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.ItemDeactivationReason'])),
            ('other_reason', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'items', ['ItemDeactivationHistory'])

        # Adding model 'ItemEditReason'
        db.create_table(u'items_itemeditreason', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reason', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'items', ['ItemEditReason'])

        # Adding model 'ItemEditHistory'
        db.create_table(u'items_itemedithistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.Item'])),
            ('moderator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customauth.CustomUser'])),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')()),
            ('reason', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.ItemEditReason'])),
            ('other_reason', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('old_value', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'items', ['ItemEditHistory'])

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

        # Adding model 'ItemUsageExperience'
        db.create_table(u'items_itemusageexperience', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customauth.CustomUser'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.Item'])),
            ('duration', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['items.ItemUsageDurationType'])),
            ('rating', self.gf('django.db.models.fields.related.ForeignKey')(default=4, to=orm['items.ItemUsageRatingType'])),
            ('date_verified', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'items', ['ItemUsageExperience'])

        # Adding model 'ItemImage'
        db.create_table(u'items_itemimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.Item'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('image_gallery_thumb', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'items', ['ItemImage'])

        # Adding unique constraint on 'ItemImage', fields ['image', 'image']
        db.create_unique(u'items_itemimage', ['image', 'image'])


    def backwards(self, orm):
        # Removing unique constraint on 'ItemImage', fields ['image', 'image']
        db.delete_unique(u'items_itemimage', ['image', 'image'])

        # Removing unique constraint on 'ItemUsageRatingType', fields ['string', 'value']
        db.delete_unique(u'items_itemusageratingtype', ['string', 'value'])

        # Removing unique constraint on 'ItemUsageDurationType', fields ['string', 'value']
        db.delete_unique(u'items_itemusagedurationtype', ['string', 'value'])

        # Deleting model 'Category'
        db.delete_table(u'items_category')

        # Deleting model 'Item'
        db.delete_table(u'items_item')

        # Deleting model 'ItemApprovalHistory'
        db.delete_table(u'items_itemapprovalhistory')

        # Deleting model 'ItemDeactivationReason'
        db.delete_table(u'items_itemdeactivationreason')

        # Deleting model 'ItemDeactivationHistory'
        db.delete_table(u'items_itemdeactivationhistory')

        # Deleting model 'ItemEditReason'
        db.delete_table(u'items_itemeditreason')

        # Deleting model 'ItemEditHistory'
        db.delete_table(u'items_itemedithistory')

        # Deleting model 'ItemUsageDurationType'
        db.delete_table(u'items_itemusagedurationtype')

        # Deleting model 'ItemUsageRatingType'
        db.delete_table(u'items_itemusageratingtype')

        # Deleting model 'ItemUsageExperience'
        db.delete_table(u'items_itemusageexperience')

        # Deleting model 'ItemImage'
        db.delete_table(u'items_itemimage')


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
            'cons_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'cover_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cover_image'", 'null': 'True', 'to': u"orm['items.ItemImage']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customauth.CustomUser']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latest_feedback': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'items_latest_set'", 'null': 'True', 'to': u"orm['reviews.Feedback']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'possible_duplicates': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'pros_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.Item']"}),
            'moderator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customauth.CustomUser']"}),
            'other_reason': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
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