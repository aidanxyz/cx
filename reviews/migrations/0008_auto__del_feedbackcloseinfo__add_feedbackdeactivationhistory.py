# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'FeedbackCloseInfo'
        db.delete_table(u'reviews_feedbackcloseinfo')

        # Adding model 'FeedbackDeactivationHistory'
        db.create_table(u'reviews_feedbackdeactivationhistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feedback', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Feedback'])),
            ('closed_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customauth.CustomUser'])),
            ('date_closed', self.gf('django.db.models.fields.DateTimeField')()),
            ('reason', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.FeedbackEditReason'])),
        ))
        db.send_create_signal(u'reviews', ['FeedbackDeactivationHistory'])


    def backwards(self, orm):
        # Adding model 'FeedbackCloseInfo'
        db.create_table(u'reviews_feedbackcloseinfo', (
            ('date_closed', self.gf('django.db.models.fields.DateTimeField')()),
            ('feedback', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Feedback'])),
            ('closed_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customauth.CustomUser'])),
            ('reason', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.FeedbackEditReason'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'reviews', ['FeedbackCloseInfo'])

        # Deleting model 'FeedbackDeactivationHistory'
        db.delete_table(u'reviews_feedbackdeactivationhistory')


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
            'possible_duplicates': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['items.ItemPossibleDuplicates']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'pros_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'views_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
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
            'Meta': {'unique_together': "(('string', 'value'),)", 'object_name': 'ItemUsageRatingType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'string': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'value': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'reviews.detail': {
            'Meta': {'ordering': "('-date_written',)", 'object_name': 'Detail'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'date_written': ('django.db.models.fields.DateTimeField', [], {}),
            'feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Feedback']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'written_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customauth.CustomUser']"})
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
        },
        u'reviews.feedbackdeactivationhistory': {
            'Meta': {'object_name': 'FeedbackDeactivationHistory'},
            'closed_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customauth.CustomUser']"}),
            'date_closed': ('django.db.models.fields.DateTimeField', [], {}),
            'feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Feedback']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.FeedbackEditReason']"})
        },
        u'reviews.feedbackedithistory': {
            'Meta': {'object_name': 'FeedbackEditHistory'},
            'date_edited': ('django.db.models.fields.DateTimeField', [], {}),
            'edited_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customauth.CustomUser']"}),
            'feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Feedback']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_value': ('django.db.models.fields.CharField', [], {'max_length': '144'})
        },
        u'reviews.feedbackeditreason': {
            'Meta': {'object_name': 'FeedbackEditReason'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'reviews.priority': {
            'Meta': {'unique_together': "(('feedback', 'marked_by'),)", 'object_name': 'Priority'},
            'date_marked': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Feedback']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marked_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customauth.CustomUser']"}),
            'value': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'reviews.vote': {
            'Meta': {'unique_together': "(('feedback', 'voted_by'),)", 'object_name': 'Vote'},
            'date_voted': ('django.db.models.fields.DateTimeField', [], {}),
            'feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Feedback']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.VoteType']"}),
            'voted_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customauth.CustomUser']"})
        },
        u'reviews.votetype': {
            'Meta': {'object_name': 'VoteType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'weight': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['reviews']