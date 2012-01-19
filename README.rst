===============
Django Bulk Export
===============

Prerequisite

Install Django celery on your system  (http://ask.github.com/django-celery/)

Include sendfile in your application library   (https://github.com/johnsensible/django-sendfile)
 
Include django-bulk-export in your application library


Include 'djcelery', 'sendfile', and 'django_bulk_celery' in your installed apps settings

Add bulk_export.js (/django-bulk-export/django_bulk_export/media/js/bulk_export.js) to your template

Define BULK_EXPORT_DIR (path to define where output file should be saved) in your settings

Define BULKEXPORT_EXPIRES=20 in settings  // the time in seconds after which you want the catche key named file to be rebuilt


Define BULKEXPORT_SESSION_COUNT=3 in settings  //the number of sessions a user is allowed to establish

Include following line in your urls.py 
	url(r'^bulkexport/', include('django_bulk_export.urls')),


Now we are done with all kinds of setup for our django_bulk_celery:

To make this work, follow the given steps:

1)Make Object of the Downloader
	var a=Downloader;

2)Define the arguments to the api using bulk_export as associative array
	a.bulk_export['task_name']='apps.myfiledownload';
	a.bulk_export['click_button']='#click';
	a.bulk_export['cancel_button']="#cancel";
	a.bulk_export['period_start']=0
	a.bulk_export['period_int']=2000;
	a.bulk_export['callback']='myfunction()';
	a.bulk_export['error_callback']='myerrorfunction()';
	a.bulk_export['catche_func']='apps.utils.hashfunc';
	a.bulk_export['request_data']='&myname=django'
	a.bulk_export['params']={'salutation':'hello'}   //The name used here should be fetched via post data in your 'apps.myfiledownload' function

3)Now run the trigger function passing to bulk_export as it parameters:
	a.trigger(a.bulk_export)
	

