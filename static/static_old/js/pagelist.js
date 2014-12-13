// JScript 文件


function change(){
var newpaper_id=document.getElementById ("newpaper_id");
var span =document.getElementById("span");
var newpaper_time = document.getElementById("newpaper_time");
if(newpaper_id.value==""){alert("请输入期数！");return false;}
var http = new HTTPRequest();
http.send("action/changepapertime.aspx?time="+escape(newpaper_time.value) + "&oldpaper_id="+span.innerHTML,"","post");
http.onresponse = function(request) {
    http.send("action/check_paper_id.aspx?paper_id="+newpaper_id.value);
    http.onresponse=function(request){
        if(request.responseText=="no"){
            http.send("action/change_id.aspx?newpaper_id="+newpaper_id.value+"&oldpaper_id="+span.innerHTML,"","post");
            http.onresponse=function(request1){
                if(request1.responseText=="ok"){
                    http.send("container/pagelist.aspx?paper_id="+newpaper_id.value)
                    http.onresponse=function(request1){
                        document.getElementById("container").innerHTML=request1.responseText;
                        changepage('refresh');
                    }
                }
                else {alert("error");}
            }
        }
        else {alert("该期数已存在");}
    }
}
return false;
}

function modify(word){
var showpaper=document.getElementById ("showpaper");
var changepaper=document.getElementById ("changepaper");
if(word=="mo"){
showpaper.style.display="none";
changepaper.style .display ="block";
}
if(word=="unmo"){
showpaper.style.display="block";
changepaper.style .display ="none";
}
return false;
}

function addpage(word){
var addpagediv=document.getElementById ("addpagediv");
if(word=="yes"){addpagediv.style .display ="block";}
else if(word=="no") {addpagediv.style .display ="none";}
}

function addpage2(){
var page_num=document.getElementById("page_num");
var page_name=document.getElementById("page_name");
if(page_num.value==""){alert("请输入版数");return false;}
if(page_name.value==""){alert("请输入版名");return false;}
var paper_num=document.getElementById("span");
var http=new HTTPRequest();
http.send("action/check_page_id.aspx?page_num="+page_num.value+"&paper_num="+paper_num.innerHTML+"&page_name="+escape(page_name.value),"","post");
http.onresponse=function(request){
if(request.responseText=="yes"){alert("该版数已存在");}

else{window.open("page.aspx?page_id="+request.responseText,"_blank");}
}
return false;
}

function delete_page(page_id,paper_num){
if(confirm("确定要删除?")==true){
var http=new HTTPRequest()
http.send("action/delete_page.aspx?page_id="+page_id);
http.onresponse=function(request){
if(request.responseText=="ok"){
http.send("container/pagelist.aspx?paper_id="+paper_num);
http.onresponse=function(request1){

document.getElementById("container").innerHTML=request1.responseText;
}
}
else {alert("删除失败");}
}
}
}