# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding unique constraint on 'TaskAuthentication', fields ['task_id']
        db.create_unique(u'task_authentication', ['task_id'])
    
    
    def backwards(self, orm):
        
        # Removing unique constraint on 'TaskAuthentication', fields ['task_id']
        db.delete_unique(u'task_authentication', ['task_id'])
    
    
    models = {
        'django_bulk_export.taskauthentication': {
            'Meta': {'object_name': 'TaskAuthentication', 'db_table': "u'task_authentication'"},
            'completion_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'filepath': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'task_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }
    
    complete_apps = ['django_bulk_export']
