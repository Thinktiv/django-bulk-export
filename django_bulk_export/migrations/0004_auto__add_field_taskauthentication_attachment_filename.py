# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'TaskAuthentication.attachment_filename'
        db.add_column(u'task_authentication', 'attachment_filename', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'TaskAuthentication.attachment_filename'
        db.delete_column(u'task_authentication', 'attachment_filename')
    
    
    models = {
        'django_bulk_export.taskauthentication': {
            'Meta': {'object_name': 'TaskAuthentication', 'db_table': "u'task_authentication'"},
            'attachment_filename': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'completion_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'filepath': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'task_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }
    
    complete_apps = ['django_bulk_export']
