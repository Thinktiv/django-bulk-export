# Create your views here.
from celery.task import task
import datetime
import md5
import csv
import os
import logging
import re

from django_bulk_export.conf import BULK_EXPORT_DIR

@task
def execute(task_name, params, filename):
    """
    Wrapper for the actual tasks. It gets the data from project task and writes to filesystem.
    """
    

    path = get_file_path(filename, params)

    if(os.path.isfile(path)):
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
    
def get_file_path(filename, params):
    """
        returns the file path to write the data into.
        TODO: Need to fix the file name computation.
    """
    filename=re.sub(r'sEcho=\d+&','',filename)
    filename=re.sub(r'iDisplayLength=\d+','',filename)
    filename=re.sub(r'iDisplayStart=\d+','',filename)
    filename=md5.new(filename)
    filename=filename.hexdigest()

    path=os.path.join(BULK_EXPORT_DIR, "%s.csv"%filename)
    return path