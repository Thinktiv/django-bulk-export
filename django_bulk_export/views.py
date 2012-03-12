# Create your views here.
from celery.result import AsyncResult
from celery.task.control import revoke
from django.utils import simplejson as json
from django.http import HttpResponse
import logging
from django_bulk_export.models import *
from sendfile import sendfile
from django_bulk_export.tasks import execute,get_or_create_tasklog, get_user_id
from django_bulk_export.constants import *

from django.contrib.auth.decorators import login_required
import settings

@login_required
def trigger(request,task_name,cache_func='',params={}):
    """
    Appends a task to the queue.
    """
    req={}
    task_log_count=TaskAuthentication.objects.filter(user_id=get_user_id(request), status=TASK_RUNNING).count()
    if task_log_count>settings.BULKEXPORT_SESSION_COUNT:
        response = json.dumps({'error_message':'You have too many sessions'})
        return HttpResponse(response, mimetype="application/json")

    #update two dictionaries
    params.update(request.REQUEST.copy())
    
    result=execute.delay(task_name,params,request.get_full_path(),cache_func,get_user_id(request)) #Support both GET/POST params
    get_or_create_tasklog(get_user_id(request),result.task_id)
    
    if request.is_ajax():
        response = json.dumps({'task_id':result.task_id})
        logging.debug("Queued task : %s"%result.task_id)
        return HttpResponse(response, mimetype="application/json")
    else:
        return result.task_id

@login_required
def status(request, task_id):
    """
    Returns status of a queued task.
    """
    res={}
    task_log=TaskAuthentication.objects.get(task_id=task_id)
    if task_log.user_id==get_user_id(request):
        result=AsyncResult(task_id)
        
        res['status']=TASK_NEW #no such tasks in queue

        if result:
            if(result.ready()):
                if(result.successful()):
                    result=result.get()
                    if isinstance(result,dict):
                        res['status']=TASK_FAILED
                        res['error_message']=result['error_message']
                    else:
                         res['status']=TASK_SUCCESSFUL #succcessfull

            else:
                 res['status']=TASK_RUNNING #waiting in queue
    else:
        logging.debug("Unauthorized User")
        res['status']=TASK_UNKNOWN
    response = json.dumps(res)
    return HttpResponse(response, mimetype="application/json")


@login_required
def cancel(request,task_id):
    """
    Cancels a queued task.
    """
    task_log=TaskAuthentication.objects.get(task_id=task_id)
    if task_log.user_id==get_user_id(request):
        logging.debug("Terminating task : %s"%task_id)
        revoke(task_id,terminate=True)
        task_log.update_fields(status=TASK_ABORTED)
        logging.debug("Terminated task : %s"%task_id)
        return HttpResponse('cancelled')
    else:
        #logging.debug("Unauthorized user %s tries to cancel task %s"%(get_user_id(request),task_id))
        return HttpResponse('You are not authorized to cancel this task')


@login_required
def download(request,task_id):
    """
    Sends the data file for a successfully executed task.
    """
    task_log=TaskAuthentication.objects.get(task_id=task_id)
    if task_log.user_id==get_user_id(request):
        file_url=task_log.filepath
        #logging.debug("Sending file : %s"%file_url)
        return sendfile(request,file_url, attachment=True)
    else:
        #logging.debug("Unauthorized user tries to download file")
        return HttpResponse("Sorry! You are not authorized to view this file")
 

@login_required
def cancel_status_change(request,task_id):
        task_log=TaskAuthentication.objects.get(task_id=task_id)
        if task_log.user_id==get_user_id(request):
            task_log.update_fields(status=TASK_NEW)
            return HttpResponse("Cancel status changed")
        else:
            return HttpResponse("Unauthorized User")