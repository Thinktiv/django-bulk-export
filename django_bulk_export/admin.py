from django.contrib import admin
from django_bulk_export.models import TaskAuthentication

class TaskAuthenticationAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'user_id', 'status', 'completion_date')
    list_filter = ('status',)

admin.site.register(TaskAuthentication, TaskAuthenticationAdmin)


