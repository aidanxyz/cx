# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feedback'
        db.create_table(u'reviews_feedback', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('body', self.gf('django.db.models.fields.CharField')(unique=True, max_length=144)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customauth.CustomUser'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')()),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.Item'])),
            ('is_positive', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal(u'reviews', ['Feedback'])

        # Adding model 'ModerationReason'
        db.create_table(u'reviews_moderationreason', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reason', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'reviews', ['ModerationReason'])

        # Adding model 'FeedbackCloseInfo'
        db.create_table(u'reviews_feedbackcloseinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feedback', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Feedback'])),
            ('closed_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customauth.CustomUser'])),
            ('date_closed', self.gf('django.db.models.fields.DateTimeField')()),
            ('reason', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.ModerationReason'])),
        ))
        db.send_create_signal(u'reviews', ['FeedbackCloseInfo'])

        # Adding model 'FeedbackEditInfo'
        db.create_table(u'reviews_feedbackeditinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feedback', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Feedback'])),
            ('edited_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customauth.CustomUser'])),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')()),
            ('old_value', self.gf('django.db.models.fields.CharField')(max_length=144)),
        ))
        db.send_create_signal(u'reviews', ['FeedbackEditInfo'])


    def backwards(self, orm):
        # Deleting model 'Feedback'
        db.delete_table(u'reviews_feedback')

        # Deleting model 'ModerationReason'
        db.delete_table(u'reviews_moderationreason')

        # Deleting model 'FeedbackCloseInfo'
        db.delete_table(u'reviews_feedbackcloseinfo')

        # Deleting model 'FeedbackEditInfo'
        db.delete_table(u'reviews_feedbackeditinfo')


    models = {
        u'customauth.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
        u'reviews.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'body': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '144'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customauth.CustomUser']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
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
        }
    }

    complete_apps = ['reviews']