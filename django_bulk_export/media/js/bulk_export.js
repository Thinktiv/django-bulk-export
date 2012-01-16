var bulk_export_downloader_track={};


var Downloader=
{

bulker_export:{params:{}},

trigger:function(export_dict)
{
                postdata='';
                if(export_dict['task_name'])
                    task_name=export_dict['task_name'];
                else
                {
                    alert("You have not defined task_name, its mandatory");
                    return false;
                }
                if(export_dict['click_button'])
                    click_button=export_dict['click_button'];
                else
                {
                    alert("You have not defined click_button, its mandatory");
                    return false;
                }
                if(export_dict['cancel_button'])
                    cancel_button=export_dict['cancel_button'];
                else
                    cancel_button='';
                if(export_dict['period_start'])
                    period_start=export_dict['period_start'];
                else
                    period_start=0;
                if(export_dict['period_int'])
                    period_int=export_dict['period_int'];
                else
                    period_int=0;
                if(export_dict['callback'])
                    callback=export_dict['callback'];
                else
                    callback='';
                if(export_dict['error_callback'])
                    error_callback=export_dict['error_callback'];
                else
                    error_callback='';
                if(export_dict['cache_func'])
                    cache_func=export_dict['cache_func'];
                else
                    cache_func='';
                if(export_dict['request_data'])
                    post=export_dict['request_data'];
                else
                    post='';
                for (key in export_dict['params'])
                {
                    postdata+='&'+key+'='+export_dict['params'][key];
                    }
                post+=postdata
                mylocation='/bulkexport/trigger/'+task_name+'/'+cache_func+'/?'+post;
                                $.ajax({
                                            "datatype":'json',
                                            "type":"POST",
                                            "url":mylocation,
                                            "success":function(json){
                                              bulk_export_downloader_track[json.task_id]='1';
                                              Downloader.cancel_joshqueue(json.task_id,click_button,cancel_button);
                                              $(click_button).hide();
                                              $(cancel_button).show();
                                              Downloader.check_status(json.task_id,click_button,cancel_button,period_start,period_int,callback,error_callback)


                                            }
                                });
},


check_status:function(task_id,click_button,cancel_button,period_start,period_int,callback,error_callback)
{

            mylocation='/bulkexport/status/'+task_id+'/'
            check_str='Downloader.check_status("'+task_id+'","'+click_button+'","'+cancel_button+'","'+period_start+'","'+period_int+'","'+callback+'","'+error_callback+'")';


                                    $.ajax({
                                            "datatype":'json',
                                            "type":"POST",
                                            "url":mylocation,
                                            "success":function(json){
                                                if(json.status=='1' && bulk_export_downloader_track[task_id]=='1')
                                                {
                                                console.log(bulk_export_downloader_track[task_id]);
                                                setTimeout(check_str,parseInt(period_int));
                                                }
                                                else if (json.status=='5')
                                                {
                                                   $("#error_message").html(json.error_message)
                                                   $(cancel_button).hide();
                                                   $(click_button).show();
                                                   eval(callback);

                                                }
                                                else if(json.status=='4'){
                                                alert("You are not authorized to check this task");
                                                }
                                                else if(json.status=='2' && bulk_export_downloader_track[task_id]=='1')
                                                  Downloader.download(task_id,click_button,cancel_button,callback);
                                                   }

                                            });

},



cancel_joshqueue:function(task_id,click_button,cancel_button)
{

            $(cancel_button).click(function(){

                                        $.ajax({
                                            "datatype":'json',
                                            "type":"POST",
                                            "url":'/bulkexport/cancel/'+task_id+'/',
                                            "success":function(json){
                                            bulk_export_downloader_track[task_id]='3';
                                            $(cancel_button).hide();
                                            $(click_button).show();

                                         }
                                         });

            });




},



download:function(task_id,click_button,cancel_button,callback)
{
$(cancel_button).hide();
$(click_button).show();
document.location.href='/bulkexport/download/'+task_id+'/';
eval(callback);
},


}





function joshqueue()
{
postdata='';
task_name=arguments[0];
for(var x=1;x<=arguments.length-8;x++)
postdata+='&arg'+x+'='+arguments[x];
click_button=arguments[arguments.length-7];
cancel_button=arguments[arguments.length-6];
period_start=arguments[arguments.length-5];
period_int=arguments[arguments.length-4];
post=arguments[arguments.length-3];
callback=arguments[arguments.length-2];
error_callback=arguments[arguments.length-1];
post=post+postdata;


            $(click_button).click(function(){

            var a=new Downloader();
            a.trigger(task_name,click_button,cancel_button,period_start,period_int,post,callback,error_callback);





            });

}










