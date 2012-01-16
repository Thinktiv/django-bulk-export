# Create your views here.
from celery.task import task
import datetime
import time
import md5
import csv
import os
import logging
import settings

from django_bulk_export.conf import BULK_EXPORT_DIR

@task
def execute(task_name, params, url,cache_func):

    """
    Wrapper for the actual tasks. It gets the data from project task and writes to filesystem.
    """
    path = get_file_path(url, params,cache_func)

    if(os.path.isfile(path)):
        if(check_updated_file(path)):
            return path
    #TODO: need to timeout this file caching.

    paths = task_name.split(".")
    package = ".".join(paths[0:-1])
    m = __import__ (package,fromlist=[paths[-1]])
    func = getattr(m,paths[-1])
    logging.debug("Executing task : %s"%task_name)
    content_data = func(params)
    if isinstance(content_data,dict):
         return content_data

    writer=csv.writer(open(path,'wb'))
    for cdata in content_data:
        writer.writerow(cdata)
    return path
    
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
        #filename=re.sub(r'sEcho=\d+&','',url)
        #filename=re.sub(r'iDisplayLength=\d+','',filename)
        #filename=re.sub(r'iDisplayStart=\d+','',filename)
        filename=default_get_cache_name(url)
    path=os.path.join(BULK_EXPORT_DIR, "%s.csv"%filename)
    return path



def default_get_cache_name(url):
    filename=filename+ datetime.datetime.now().strftime("%m %d %Y %H %M %S")
    filename=md5.new(url)
    filename=filename.hexdigest()
    return filename


def check_updated_file(path):
    try:
        file_timestamp=os.path.getmtime(path)
        now_timestamp=time.mktime(datetime.datetime.now().timetuple())
        if (settings.BULKEXPORT_EXPIRES>(now_timestamp-file_timestamp)):
            return True
    except:
        pass
    return False