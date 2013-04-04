# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Priority'
        db.create_table(u'reviews_priority', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feedback', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Feedback'])),
            ('marked_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customauth.CustomUser'])),
            ('value', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('date_marked', self.gf('django.db.models.fields.DateTimeField')()),
            ('feedback_item_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.Item'])),
        ))
        db.send_create_signal(u'reviews', ['Priority'])

        # Adding unique constraint on 'Priority', fields ['feedback', 'marked_by']
        db.create_unique(u'reviews_priority', ['feedback_id', 'marked_by_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Priority', fields ['feedback', 'marked_by']
        db.delete_unique(u'reviews_priority', ['feedback_id', 'marked_by_id'])

        # Deleting model 'Priority'
        db.delete_table(u'reviews_priority')


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
            'body': ('django.db.models.fields.CharField', [], {'max_length': '144'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customauth.CustomUser']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_positive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.Item']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'reviews.feedbackcloseinfo': {
            'Meta': {'object_name': 'FeedbackCloseInfo'},
            'closed_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customauth.CustomUser']"}),
            'date_closed': ('django.db.models.fields.DateTimeField', [], {}),
            'feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Feedback']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.ModerationReason']"})
        },
        u'reviews.feedbackeditinfo': {
            'Meta': {'object_name': 'FeedbackEditInfo'},
            'date_edited': ('django.db.models.fields.DateTimeField', [], {}),
            'edited_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customauth.CustomUser']"}),
            'feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Feedback']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_value': ('django.db.models.fields.CharField', [], {'max_length': '144'})
        },
        u'reviews.moderationreason': {
            'Meta': {'object_name': 'ModerationReason'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'reviews.priority': {
            'Meta': {'unique_together': "(('feedback', 'marked_by'),)", 'object_name': 'Priority'},
            'date_marked': ('django.db.models.fields.DateTimeField', [], {}),
            'feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Feedback']"}),
            'feedback_item_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.Item']"}),
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