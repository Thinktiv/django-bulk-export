from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('django_bulk_export.views',

    # Uncomment the next line to enable the admin:
    url(r'^trigger/(?P<task_name>[.\w]+)/(?P<cache_func>[_.\w]*)/(?P<attachment_filename>[_.\w]*)/$','trigger',  name='django-bulk-export_trigger'),
    url(r'^status/(?P<task_id>[-\w]+)/$','status',  name='django-bulk-export_status'),
    url(r'^cancel/(?P<task_id>[-\w]+)/$','cancel',  name='django-bulk-export_cancel'),
    url(r'^download/(?P<task_id>[-\w]+)/$','download',  name='django-bulk-export_download'),
    url(r'^cancelstatus/(?P<task_id>[-\w]+)/$','cancel_status_change',  name='django-bulk-export_download'),
)