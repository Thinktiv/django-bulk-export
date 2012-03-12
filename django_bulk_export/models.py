from django.db import models
import datetime
from django_bulk_export.constants import STATUS_CHOICES, TASK_NEW

class TaskAuthentication(models.Model):
    user_id=models.CharField(max_length=128)
    task_id=models.CharField(max_length=128,unique=True)
    filepath=models.CharField(max_length=200,blank=True, null=True)
    status=models.IntegerField(choices=STATUS_CHOICES, default=TASK_NEW)
    completion_date=models.DateTimeField('Task completion date',blank=True, null=True)

    def __unicode__(self):
        return self.task_id

    def update_fields(self, **kwargs):
        for field in kwargs:
            setattr(self, field, kwargs[field])
        return self.save()

    class Meta:
        db_table = u'task_authentication'
    