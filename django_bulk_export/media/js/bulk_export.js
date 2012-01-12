//include it as js file in your app



function Downloader()
{
 
}



Downloader.prototype.trigger=function()
{
    postdata='';
    task_name=arguments[0];
    for(var x=1;x<=arguments.length-6;x++)
        postdata+='&arg'+x+'='+arguments[x];
    cancel_button=arguments[arguments.length-5];
    period_start=arguments[arguments.length-4];
    period_int=arguments[arguments.length-3];
    post=arguments[arguments.length-2];
    callback=arguments[arguments.length-1];
    post+=postdata

    mylocation='/me/trigger/'+task_name+'/?'+post;
    $.ajax({
        "datatype":'json',
        "type":"POST",
        "url":mylocation,
        "success":function(json){

            cancel_joshqueue(json.task_id,cancel_button);
            check_status(json.task_id,period_start,period_int,callback)


        }
    });
}


function joshqueue()
{
    postdata='';
    task_name=arguments[0];
    for(var x=1;x<=arguments.length-7;x++)
        postdata+='&arg'+x+'='+arguments[x];
    click_button=arguments[arguments.length-6];
    cancel_button=arguments[arguments.length-5];
    period_start=arguments[arguments.length-4];
    period_int=arguments[arguments.length-3];
    post=arguments[arguments.length-2];
    callback=arguments[arguments.length-1];
    post=post+postdata;


    $(click_button).click(function(){
           
        var a=new Downloader();
        a.trigger(task_name,cancel_button,period_start,period_int,post,callback);





    });

}



function check_status(task_id,period_start,period_int,callback)
{
    mylocation='/me/status/'+task_id+'/'
    check_str='check_status("'+task_id+'","'+period_start+'","'+period_int+'","'+callback+'")';

    $.ajax({
        "datatype":'json',
        "type":"POST",
        "url":mylocation,
        "success":function(json){
            if(json.status=='1')
                setTimeout(check_str,parseInt(period_int));
            else
            {
                                                
                download(task_id);
            }
        }

    });

}





function cancel_joshqueue(task_id,cancel_button)
{      
            
    $(cancel_button).click(function(){

        $.ajax({
            "datatype":'json',
            "type":"POST",
            "url":'/me/cancel/'+task_id+'/',
            "success":function(json){

                                            
            }
        });

    });




}


function download(task_id)
{
    document.location.href='/me/download/'+task_id+'/';

}
