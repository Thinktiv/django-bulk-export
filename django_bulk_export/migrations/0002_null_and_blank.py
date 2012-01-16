# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Changing field 'TaskAuthentication.filepath'
        db.alter_column(u'task_authentication', 'filepath', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True))

        # Changing field 'TaskAuthentication.completion_date'
        db.alter_column(u'task_authentication', 'completion_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True))
    
    
    def backwards(self, orm):
        
        # Changing field 'TaskAuthentication.filepath'
        db.alter_column(u'task_authentication', 'filepath', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'TaskAuthentication.completion_date'
        db.alter_column(u'task_authentication', 'completion_date', self.gf('django.db.models.fields.DateTimeField')())
    
    
    models = {
        'django_bulk_export.taskauthentication': {
            'Meta': {'object_name': 'TaskAuthentication', 'db_table': "u'task_authentication'"},
            'completion_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'filepath': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }
    
    complete_apps = ['django_bulk_export']
