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
            ('body', self.gf('django.db.models.fields.CharField')(max_length=144)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customauth.CustomUser'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')()),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.Item'])),
            ('is_positive', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'reviews', ['Feedback'])

        # Adding unique constraint on 'Feedback', fields ['body', 'item', 'is_positive']
        db.create_unique(u'reviews_feedback', ['body', 'item_id', 'is_positive'])

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

        # Adding model 'VoteType'
        db.create_table(u'reviews_votetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('weight', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'reviews', ['VoteType'])

        # Adding model 'Vote'
        db.create_table(u'reviews_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feedback', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Feedback'])),
            ('voted_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customauth.CustomUser'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.VoteType'])),
            ('date_voted', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'reviews', ['Vote'])

        # Adding unique constraint on 'Vote', fields ['feedback', 'voted_by']
        db.create_unique(u'reviews_vote', ['feedback_id', 'voted_by_id'])

        # Adding model 'Detail'
        db.create_table(u'reviews_detail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('feedback', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Feedback'])),
            ('written_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customauth.CustomUser'])),
            ('date_written', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'reviews', ['Detail'])

        # Adding model 'Favorite'
        db.create_table(u'reviews_favorite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.Item'])),
            ('feedback', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Feedback'])),
            ('feedback_type', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('marked_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customauth.CustomUser'])),
            ('date_marked', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'reviews', ['Favorite'])

        # Adding unique constraint on 'Favorite', fields ['feedback', 'marked_by']
        db.create_unique(u'reviews_favorite', ['feedback_id', 'marked_by_id'])

        # Adding unique constraint on 'Favorite', fields ['item', 'feedback_type']
        db.create_unique(u'reviews_favorite', ['item_id', 'feedback_type'])


    def backwards(self, orm):
        # Removing unique constraint on 'Favorite', fields ['item', 'feedback_type']
        db.delete_unique(u'reviews_favorite', ['item_id', 'feedback_type'])

        # Removing unique constraint on 'Favorite', fields ['feedback', 'marked_by']
        db.delete_unique(u'reviews_favorite', ['feedback_id', 'marked_by_id'])

        # Removing unique constraint on 'Vote', fields ['feedback', 'voted_by']
        db.delete_unique(u'reviews_vote', ['feedback_id', 'voted_by_id'])

        # Removing unique constraint on 'Feedback', fields ['body', 'item', 'is_positive']
        db.delete_unique(u'reviews_feedback', ['body', 'item_id', 'is_positive'])

        # Deleting model 'Feedback'
        db.delete_table(u'reviews_feedback')

        # Deleting model 'ModerationReason'
        db.delete_table(u'reviews_moderationreason')

        # Deleting model 'FeedbackCloseInfo'
        db.delete_table(u'reviews_feedbackcloseinfo')

        # Deleting model 'FeedbackEditInfo'
        db.delete_table(u'reviews_feedbackeditinfo')

        # Deleting model 'VoteType'
        db.delete_table(u'reviews_votetype')

        # Deleting model 'Vote'
        db.delete_table(u'reviews_vote')

        # Deleting model 'Detail'
        db.delete_table(u'reviews_detail')

        # Deleting model 'Favorite'
        db.delete_table(u'reviews_favorite')


    models = {
        u'customauth.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'items_used': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['items.Item']", 'through': u"orm['customauth.ItemUsageExperience']", 'symmetrical': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'customauth.itemusageexperience': {
            'Meta': {'object_name': 'ItemUsageExperience'},
            'duration': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.Item']"}),
            'rating': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customauth.CustomUser']"})
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
        u'reviews.detail': {
            'Meta': {'ordering': "('-date_written',)", 'object_name': 'Detail'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'date_written': ('django.db.models.fields.DateTimeField', [], {}),
            'feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Feedback']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'written_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customauth.CustomUser']"})
        },
        u'reviews.favorite': {
            'Meta': {'unique_together': "(('feedback', 'marked_by'), ('item', 'feedback_type'))", 'object_name': 'Favorite'},
            'date_marked': ('django.db.models.fields.DateTimeField', [], {}),
            'feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reviews.Feedback']"}),
            'feedback_type': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['items.Item']"}),
            'marked_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customauth.CustomUser']"})
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