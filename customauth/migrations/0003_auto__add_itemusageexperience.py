# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ItemUsageExperience'
        db.create_table(u'customauth_itemusageexperience', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customauth.CustomUser'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['items.Item'])),
            ('duration', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('rating', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'customauth', ['ItemUsageExperience'])

        # Removing M2M table for field items_used on 'CustomUser'
        db.delete_table('customauth_customuser_items_used')


    def backwards(self, orm):
        # Deleting model 'ItemUsageExperience'
        db.delete_table(u'customauth_itemusageexperience')

        # Adding M2M table for field items_used on 'CustomUser'
        db.create_table(u'customauth_customuser_items_used', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customuser', models.ForeignKey(orm[u'customauth.customuser'], null=False)),
            ('item', models.ForeignKey(orm[u'items.item'], null=False))
        ))
        db.create_unique(u'customauth_customuser_items_used', ['customuser_id', 'item_id'])


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
        }
    }

    complete_apps = ['customauth']