# Create your views here.
from celery.result import AsyncResult
from celery.task.control import revoke
from django.utils import simplejson as json
from django.http import HttpResponse
import logging
from django_bulk_export.models import *
from sendfile import sendfile
import datetime
from django_bulk_export.tasks import execute
from django.contrib.auth.decorators import login_required
import settings

@login_required
def trigger(request,task_name,cache_func):
    """
    Appends a task to the queue.
    """
    req={}
    user_auth_count=TaskAuthentication.objects.filter(user_id=request.META['REMOTE_ADDR'], status=1).count()
    if user_auth_count>settings.BULKEXPORT_SESSION_COUNT:
        response = json.dumps({'error_message':'You have too many sessions'})
        return HttpResponse(response, mimetype="application/json")

    result=execute.delay(task_name,request.GET.copy(),request.get_full_path(),cache_func) #Support both GET/POST params
    db_logging(request,result.task_id)
    response = json.dumps({'task_id':result.task_id})
    logging.debug("Queued task : %s"%result.task_id)
    
    return HttpResponse(response, mimetype="application/json")

@login_required
def status(request, task_id):
    """
    Returns status of a queued task.
    """
    req={}
    user_auth=TaskAuthentication.objects.get(task_id=task_id)
    if user_auth.user_id==request.META['REMOTE_ADDR']:
        logging.debug("Autherized User")
        result=AsyncResult(task_id)
        
        req['status']=0 #no such tasks

        if result:
            if(result.ready()):
                if(result.successful()):
                    result=result.get()
                    if isinstance(result,dict):
                        user_auth.status=5
                        user_auth.save()
                        req['status']=5
                        req['error_message']=result['error_message']
                    else:
                        user_auth.status=2
                        user_auth.filepath=result
                        user_auth.save()
                        req['status']=2 #succcessfull


            else:
                user_auth.status=1
                user_auth.save()
                req['status']=1 #waiting in queue
    else:
        logging.debug("Unauthorized User")
        user_auth.status=4
        user_auth.save()
        req['status']=4
    user_auth.completion_date=datetime.datetime.now()
    user_auth.save()
    response = json.dumps(req)
    return HttpResponse(response, mimetype="application/json")


@login_required
def cancel(request,task_id):
    """
    Cancels a queued task.
    """
    user_auth=TaskAuthentication.objects.get(task_id=task_id)
    if user_auth.user_id==request.META['REMOTE_ADDR']:
        logging.debug("Terminating task : %s"%task_id)
        revoke(task_id,terminate=True)
        logging.debug("Terminated task : %s"%task_id)
        return HttpResponse('cancelled')
    else:
        logging.debug("Unauthorized user %s tries to cancel task %s"%(request.META['REMOTE_ADDR'],task_id))
        return HttpResponse('You are not authorized to cancel this task')

@login_required
def download(request,task_id):
    """
    Sends the data file for a successfully executed task.
    """
    user_auth=TaskAuthentication.objects.get(task_id=task_id)
    if user_auth.user_id==request.META['REMOTE_ADDR']:
        file_url=user_auth.filepath
        logging.debug("Sending file : %s"%file_url)
        return sendfile(request,file_url, attachment=True)
    else:
        logging.debug("Unauthorized user tries to download file")
        return HttpResponse("Sorry! You are not authorized to view this file")

 
def db_logging(request,task_id):
    logging.debug("Client IP:%s"%request.META['REMOTE_ADDR'])
    TaskAuthentication.objects.create(user_id=request.META['REMOTE_ADDR'],task_id=task_id,status=0)

@login_required
def cancel_status_change(request,task_id):
        user_auth=TaskAuthentication.objects.get(task_id=task_id)
        if user_auth.user_id==request.META['REMOTE_ADDR']:
            user_auth.status=0
            user_auth.save()
            return HttpResponse("Cancel status changed")
        else:
            return HttpResponse("Unauthorized User")