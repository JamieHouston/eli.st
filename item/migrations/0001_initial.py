# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Attribute'
        db.create_table('item_attribute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('item', ['Attribute'])

        # Adding model 'Item'
        db.create_table('item_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.CustomUser'])),
        ))
        db.send_create_signal('item', ['Item'])

        # Adding model 'ItemAttribute'
        db.create_table('item_itemattribute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attribute', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['item.Attribute'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['item.Item'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('item', ['ItemAttribute'])

    def backwards(self, orm):
        # Deleting model 'Attribute'
        db.delete_table('item_attribute')

        # Deleting model 'Item'
        db.delete_table('item_item')

        # Deleting model 'ItemAttribute'
        db.delete_table('item_itemattribute')

    models = {
        'account.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'item.attribute': {
            'Meta': {'object_name': 'Attribute'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'item.item': {
            'Meta': {'object_name': 'Item'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['item.Attribute']", 'through': "orm['item.ItemAttribute']", 'symmetrical': 'False'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.CustomUser']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'item.itemattribute': {
            'Meta': {'object_name': 'ItemAttribute'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['item.Attribute']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['item.Item']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['item']