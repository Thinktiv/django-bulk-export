# Create your views here.
from celery.task import task
import datetime
import md5
import csv
import os
import logging


from django_bulk_export.conf import BULK_EXPORT_DIR

@task
def execute(task_name, params):
    """
    Wrapper for the actual tasks. It gets the data from project task and writes to filesystem.
    """
    paths = task_name.split(".")
    package = ".".join(paths[0:-1])
    m = __import__ (package,fromlist=[paths[-1]])
    func = getattr(m,paths[-1])
    logging.debug("Executing task : %s"%task_name)    
    content_data = func(params)
    path = get_file_path(params)
    writer=csv.writer(open(path,'wb'))
    for cdata in content_data:
        writer.writerow(cdata)
    return path
    
def get_file_path(params):
    """
        returns the file path to write the data into.
        TODO: Need to fix the file name computation.
    """
    filename=datetime.datetime.now().strftime("%d %m %Y %H %M %S")
    filename=md5.new(filename)
    filename=filename.hexdigest()
    path=os.path.join(BULK_EXPORT_DIR, "%s.csv"%filename)
    return path