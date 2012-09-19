# Create your views here.
from celery.task import task
import datetime
import time
import md5
import csv
import os
import logging
from django.conf import settings
from django_bulk_export.models import *
from django.utils.encoding import smart_str
from django_bulk_export.constants import *

@task
def execute(task_name, params, url,cache_func,user_id,attachment_filename=''):

    """
    Wrapper for the actual tasks. It gets the data from project task and writes to filesystem.
    """
    task_log=get_or_create_tasklog(user_id,execute.request.id,attachment_filename)
    task_log.update_fields(status=TASK_RUNNING)
    
    path = get_file_path(url, params,cache_func)

    if(os.path.isfile(path) and not is_file_expired(path)):
        #Check if exported file alreasy exists and not expired
        task_log.update_fields(status=TASK_SUCCESSFUL, filepath=path,
            completion_date=datetime.datetime.now())
        return path
    else:        
        task_func = get_task_func(task_name)
        logging.debug("Executing task : %s"%task_name)
        content_data = task_func(params)
        
        if isinstance(content_data,dict):  #Task failed due to some error
             task_log.update_fields(status=TASK_FAILED)
             return content_data
        else:
            dir_name = os.path.dirname(path)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            writer=csv.writer(open(path,'wb'))
            for cdata in content_data:
                writer.writerow([smart_str(cd) if cd else None for cd in cdata])
            #writer.close()
            task_log.update_fields(status=TASK_SUCCESSFUL, filepath=path,
                        completion_date=datetime.datetime.now())
            return path

def get_task_func(task_name):
    """
        returns the task function.
    """
    paths = task_name.split(".")
    package = ".".join(paths[0:-1])
    m = __import__ (package,fromlist=[paths[-1]])
    func = getattr(m,paths[-1])
    return func

def get_file_path(url, params,cache_func):
    """
        returns the file path to write the data into.
        TODO: Need to fix the file name computation.
    """
    #logging.debug('Function_name: %s'%settings.BULKEXPORT_FILENAME_FUNC)
    #user_func=settings.BULKEXPORT_FILENAME_FUNC
    if cache_func:
        paths=cache_func.split(".")
        package=".".join(paths[0:-1])
        m=__import__(package,fromlist=[paths[-1]])
        func=getattr(m,paths[-1])
        filename=func(url,params)
    else:
        filename=get_default_cache_name(url)
    path=os.path.join(BULK_EXPORT_DIR, "%s.csv"%filename)
    return path

def get_default_cache_name(url):
    filename = url + datetime.datetime.now().strftime("%m %d %Y %H %M %S")
    filename = md5.new(filename)
    filename = filename.hexdigest()
    return filename


def is_file_expired(path):
    try:
        file_timestamp=os.path.getmtime(path)
        now_timestamp=time.mktime(datetime.datetime.now().timetuple())
        if (settings.BULKEXPORT_EXPIRES>(now_timestamp-file_timestamp)):
            return False
    except:
        pass
    return True


def get_or_create_tasklog(user_id,task_id,attachment_filename=None):
    #logging.debug("Client ID:%s"%user_id)
    defaults = {'attachment_filename':attachment_filename} if attachment_filename else {}
    user_auth,created=TaskAuthentication.objects.get_or_create(user_id=user_id,task_id=task_id,defaults=defaults)
    return user_auth

def get_user_id(request):    
    return "%s"%request.user.pk
