// JScript 文件

function getpage(url) {
    var http = new HTTPRequest();
    var container = document.getElementById("container");
    http.onresponse = function(request) {
        container.innerHTML=request.responseText
    } 
    http.send(url,"","post");
    return false;
}
function gopaper(){
    var paper_num=document.getElementById("paper_num");
    var http = new HTTPRequest();
    http.onresponse=function(request){
        if(request.responseText=="yes"){
            getpage("container/pagelist.aspx?paper_id="+paper_num.value )
        }
        else {alert("该期数不存在");}
    }
    http.send("action/check_paper_id.aspx?paper_id="+paper_num.value)
    return false;
}

function ChangePageName(page_id,paper_id,pageNum,pageName){
    var http = new HTTPRequest();
    http.onresponse = function(request){
        if(request.responseText == "numerror"){
            alert("该版数已存在");
        }
        else if(request.responseText != "ok"){
            alert("error");
        }
        else{
            getpage('container/pagelist.aspx?paper_id=' + paper_id)
        }
    }
    http.send("action/ChangePageInfo.aspx?page_num=" + pageNum + "&page_name=" + escape(pageName) + "&page_id=" + page_id + "&paper_id=" +paper_id,"","post");
    return false;
}

//添加一期确定键
function addnewpaper(){
    var paper_id=document.getElementById ("paper_id");
    var paper_time = document.getElementById("paper_time");
    var http = new HTTPRequest();
     http.onresponse=function(request){
         if(request.responseText=="no"){
             http.onresponse=function(request1){

                 if(request1.responseText=="ok"){
                     http.onresponse=function(request2){
                         var container=document.getElementById ("container");
                         container.innerHTML=request2.responseText;
                         firstpage();
                     }
                     http.send("container/pagelist.aspx?paper_id="+paper_id.value,"","post");
                 }
                 else {alert("error");}
             }
             http.send("action/insert_paper_num.aspx?paper_id="+paper_id.value+"&time=" + escape(paper_time.value),"","post");
         }
         else {
             alert("期数已存在");
         }
     }
     http.send("action/check_paper_id.aspx?paper_id="+paper_id.value,"","post");
     return false;
}
function changepage(word){

    var http =new HTTPRequest();
    var spanpage =document.getElementById ("spanpage");

    var showpage=document.getElementById ("showpage");

    http.onresponse=function(request){
        showpage.innerHTML=request.responseText;
    }

    http.send("action/page.aspx?page="+(spanpage?spanpage.innerHTML:"0")+"&word="+word,"","post");
    return false;
}

function firstpage(){
    var showpage=document.getElementById ("showpage");
    var http=new HTTPRequest();
    http.onresponse=function(request){
        showpage.innerHTML=request.responseText;
    }
    http.send("action/page.aspx?word=first","","post")
}

function delete_paper(paper_num){
    if(confirm("确定删除")){
        var http=new HTTPRequest();
        http.onresponse=function(request){
            if(request.responseText=="ok"){
                changepage('refresh');
                var span =document.getElementById ("span");
                if(!span) return ;
                if(paper_num==span.innerHTML){
                    var container=document.getElementById ("container");
                    container.innerHTML="";
                }
            }
        }
        http.send("action/delete_paper.aspx?paper_num="+paper_num);
    }
    return false;
}

//发布
function Issued(paper_num,obj){
    if(confirm("确定要发布？此操作不可还原")){
        var http=new HTTPRequest();
        http.onresponse=function(request){
            if(request .responseText=="ok"){
                alert("发布成功");
                firstpage();
            }
            else{
                alert("error");
            }
        }
        http.send("action/issued.aspx?paper_num="+paper_num);
        obj.disabled = true;
    }
}

