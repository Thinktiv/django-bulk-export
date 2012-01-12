# Create your views here.
from celery.result import AsyncResult
from celery.task.control import revoke
from django.utils import simplejson as json
from django.http import HttpResponse
import logging

from sendfile import sendfile

from django_bulk_export.tasks import execute

def trigger(request,task_name):
    """
    Appends a task to the queue.
    """
    result=execute.delay(task_name,request.GET.copy(),request.get_full_path()) #Support both GET/POST params
    response = json.dumps({'task_id':result.task_id})
    logging.debug("Queued task : %s"%result.task_id)
    return HttpResponse(response, mimetype="application/json")


def status(request, task_id):
    """
    Returns status of a queued task.
    """
    result=AsyncResult(task_id)
    req={}
    req['status']=0 #no such tasks

    if result:
        if(result.ready()):
            if(result.successful()):
                result=result.get()
                if isinstance(result,dict):
                    req['status']=5
                    req['error_message']=result['error_message']
                else:
                    req['status']=2 #succcessfull
        else:
            req={}
            req['status']=1 #waiting in queue

    response = json.dumps(req)
    return HttpResponse(response, mimetype="application/json")

def cancel(request,task_id):
    """
    Cancels a queued task.
    """
    logging.debug("Terminating task : %s"%task_id)
    revoke(task_id,terminate=True)
    logging.debug("Terminated task : %s"%task_id)
    return HttpResponse('cancelled')

def download(request,task_id):
    """
    Sends the data file for a successfully executed task.
    """
    result=AsyncResult(task_id)

    if result:
        file_url=result.get()
        logging.debug("Sending file : %s"%file_url)
        return sendfile(request,file_url, attachment=True)


