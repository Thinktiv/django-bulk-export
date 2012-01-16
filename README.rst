===============
Django Bulk Export
===============

Prerequisite

Install Django celery on your system

Include sendfile in your application library

Include django-bulk-export in your application library


Include 'djcelery', 'sendfile', and 'django_bulk_celery' in your installed apps settings

Add bulk_export.js (/django-bulk-export/django_bulk_export/media/js/bulk_export.js) to your html page

Define BULK_EXPORT_DIR (path to define where file should be saved) in your settings

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
	
