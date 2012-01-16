from django.db import models
import datetime

class TaskAuthentication(models.Model):
    user_id=models.CharField(max_length=128)
    task_id=models.CharField(max_length=128)
    filepath=models.CharField(max_length=200,blank=True, null=True)
    status=models.IntegerField()
    completion_date=models.DateTimeField('Task completion date',blank=True, null=True)

    def __unicode__(self):
        return self.task_id

    class Meta:
        db_table = u'task_authentication'
    