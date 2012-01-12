//With special thanks to amit, satish, rahul and sandeep
//include this file in your js
//copy joshqueue to your main project folder
//


function Downloader()
{

}



Downloader.prototype.trigger=function()
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
    post+=postdata

    mylocation='/me/trigger/'+task_name+'/?'+post;
    $.ajax({
        "datatype":'json',
        "type":"POST",
        "url":mylocation,
        "success":function(json){

            cancel_joshqueue(json.task_id,click_button,cancel_button);
            $(click_button).hide();
            $(cancel_button).show();
            check_status(json.task_id,click_button,cancel_button,period_start,period_int,callback,error_callback)


        }
    });
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



function check_status(task_id,click_button,cancel_button,period_start,period_int,callback,error_callback)
{

    mylocation='/me/status/'+task_id+'/'
    check_str='check_status("'+task_id+'","'+click_button+'","'+cancel_button+'","'+period_start+'","'+period_int+'","'+callback+'","'+error_callback+'")';


    $.ajax({
        "datatype":'json',
        "type":"POST",
        "url":mylocation,
        "success":function(json){
            if(json.status=='1')
                setTimeout(check_str,parseInt(period_int));
            else if (json.status=='5')
            {
                $("#error_message").html(json.error_message)
                eval(callback);
            //alert(json.error_message);
            }
            else
                download(task_id,click_button,cancel_button,callback);
        }

    });

}





function cancel_joshqueue(task_id,click_button,cancel_button)
{

    $(cancel_button).click(function(){

        $.ajax({
            "datatype":'json',
            "type":"POST",
            "url":'/me/cancel/'+task_id+'/',
            "success":function(json){
                $(cancel_button).hide();
                $(click_button).show();

            }
        });

    });




}


function download(task_id,click_button,cancel_button,callback)
{
    $(cancel_button).hide();
    $(click_button).show();
    document.location.href='/me/download/'+task_id+'/';
    eval(callback);
}