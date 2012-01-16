# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'TaskAuthentication'
        db.create_table(u'task_authentication', (
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('user_id', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('task_id', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('filepath', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('completion_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('django_bulk_export', ['TaskAuthentication'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'TaskAuthentication'
        db.delete_table(u'task_authentication')
    
    
    models = {
        'django_bulk_export.taskauthentication': {
            'Meta': {'object_name': 'TaskAuthentication', 'db_table': "u'task_authentication'"},
            'completion_date': ('django.db.models.fields.DateTimeField', [], {}),
            'filepath': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }
    
    complete_apps = ['django_bulk_export']
