var TRIGGER_URL='/bulkexport/trigger/';
var STATUS_URL='/bulkexport/status/';
var CANCEL_URL='/bulkexport/cancel/';
var DOWNLOAD_URL='/bulkexport/download/';

var bulk_export_downloader_track={};
var downloader_instances_tracker={};


function BulkExport(options)
{
    if(typeof options.trigger_init=='function')
        {this.trigger_init=options.trigger_init;}
    else
        {this.trigger_init=function(){};}

    if(typeof options.trigger_task_get=='function')
        {this.trigger_task_get=options.trigger_task_get;}
    else
        {this.trigger_task_get=function(task_id){};}


    if(typeof options.trigger_task_not_get=='function')
        {this.trigger_task_not_get=options.trigger_task_not_get;}
    else
        {this.trigger_task_not_get=function(msg){};}

    if(typeof options.trigger_complete=='function')
        {this.trigger_complete=options.trigger_complete;}
    else
        {this.trigger_complete=function(){};}


    if(typeof options.trigger_error=='function')
        {this.trigger_error=options.trigger_error;}
    else
        {this.trigger_error=function(msg){};}


    if(typeof options.cancel_complete=='function')
        {this.cancel_complete=options.cancel_complete;}
    else
        {this.cancel_complete=function(){};}

    if(typeof options.cancel_init=='function')
        {this.cancel_init=options.cancel_init;}
    else
        {this.cancel_init=function(){};}

    if(typeof options.poll_init=='function')
        {this.poll_init=options.poll_init;}
    else
        {this.poll_init=function(){};}

    if(typeof options.poll_complete=='function')
        {this.poll_complete=options.poll_complete;}
    else
        {this.poll_complete=function(){};}

    if(typeof options.poll_status_waiting=='function')
        {this.poll_status_waiting=options.poll_status_waiting;}
    else
        {this.poll_status_waiting=function(status){};}


    if(typeof options.poll_error=='function')
        {this.poll_error=options.poll_error;}
    else
        {this.poll_error=function(msg){};}


    if(typeof options.download_init=='function')
        {this.download_init=options.download_init;}
    else
        {this.download_init=function(){};}

    if(typeof options.download_complete=='function')
        {this.download_complete=options.download_complete;}
    else
        {this.download_complete=function(){};}



    if(typeof options.cancel_error=='function')
        {this.cancel_error=options.cancel_error;}
    else
        {this.cancel_error=function(msg){};
     }
    if(options.start_period)
        {this.start_period=options.start_period}
    else
        {this.start_period=0;}
    if(options.period_interval)
        {this.period_interval=options.period_interval}
    else
        {this.period_interval=200;}

    this.task_id='';


    //trigger function
    this.trigger=function(task_name,params,post,cache_func){
        this.trigger_init();
        that = this;
        postdata='';
        for (key in params)
        {
          postdata+='&'+key+'='+params[key];
        }

        post=post+postdata;
        var trigger_url=TRIGGER_URL+task_name+'/'+cache_func+'/?'+post;

                    $.ajax({
                                "datatype":'json',
                                "type":"POST",
                                "url":trigger_url,
                                "success":function(json){
                                  if(json.task_id)
                                  {
                                      bulk_export_downloader_track[json.task_id]='1';
                                      that.task_id=json.task_id
                                      downloader_instances_tracker[json.task_id]=that;
                                      that.trigger_task_get(json.task_id);
                                      that.check_status();
                                      that.trigger_complete();
                                  }
                                  else
                                  {
                                       that.trigger_task_not_get("Some error occured please try after sometime...");
                                  }
                                },
                                "error":function(){
                                    that.trigger_error("Ajax Request failed");
                                }

                });
    

    };


    //polling function
    this.check_status=function(){
        task_id=this.task_id;
        that=this;        
        var status_url=STATUS_URL+task_id+'/';

        chk_str="redirect_to_check_status(\""+task_id+"\")";


                        $.ajax({
                        "datatype":'json',
                        "type":"POST",
                        "url":status_url,
                        "success":function(json){
                            if(json.status=='1' && bulk_export_downloader_track[task_id]=='1')
                            {
                            that.poll_status_waiting(json.status);
                            setTimeout(chk_str,parseInt(that.period_interval));

                            }
                            else if (json.status=='5')
                            {
                            that.poll_error(json.error_message);

                            }
                            else if(json.status=='4'){
                            that.poll_error("You are not authorized to check this task");

                            }
                            else if(json.status=='2' && bulk_export_downloader_track[task_id]=='1'){
                              that.poll_complete();
                              that.download();
                              }
                               },
                           "error":function(){
                             that.poll_error("Server Error");

                           }

                        });
    };

    //cancel function
    this.cancel=function(){
        that=this;
        this.cancel_init();
        task_id=this.task_id;
        cancel_url=CANCEL_URL+task_id+'/';
            $.ajax({
                "datatype":'json',
                "type":"POST",
                "url":cancel_url,
                "success":function(json){
                bulk_export_downloader_track[task_id]='3';
                console.log("Task Cancelled")
                that.cancel_complete();

             },
                "error":function(){
                    that.cancel_error("Error with server");
                },
            });



    };

    this.download=function(){
        task_id=this.task_id;
        this.download_init();

        document.location.href=DOWNLOAD_URL+task_id+'/';

        this.download_complete();
    };





}



// redirect to polling function
function redirect_to_check_status(task_id)
{
obj=downloader_instances_tracker[task_id];
obj.check_status();
}


 