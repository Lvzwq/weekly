//检查file控件是否为空
function pic_confirm(){
    var pic_id=document.getElementById ("uppic");
    if(pic_id.value==null||pic_id.value==""){
        alert("选择图片地址");
        return false;
    }
    //else{ ChangePic(); }
	return true;
}

function ChangePic(){
    var word = document.getElementById("get_pid");
    if(word.value != "0"){
        var http=new HTTPRequest();
        http.send("action/change_pic.aspx?page_id=" + word.value);
        http.onresponse=function(request){
            if(request.responseText != "ok"){
                alert("删除出错");
            }
        }
        
    }
}

//切换文章
function change(word){
document.getElementById("edit").style.display="block";
    document.getElementById("showarticle").style.display="none";
var newarc=document.getElementById ("newarticle");
var oldarc=document.getElementById ("oldarticle");
if(word=="new"){
newarc.style .display ="block";
oldarc.style.display="none";
}
else if(word="old"){
newarc.style .display ="none";
oldarc.style.display="block";
}
}

function showarea(page_id){
var http=new HTTPRequest();
http.send("action/showarea.aspx?page_id="+page_id,"","post");
http.onresponse=function(request){
    var picdiv=document.getElementById("picdiv");
    picdiv.innerHTML=request.responseText;
}
}

//获取文章标题
function getarticle(paper_id,page_id){
    var http=new HTTPRequest();
    http.send("action/getarticle.aspx?paper_id="+paper_id + "&page_id="+page_id,"","post");
    http.onresponse=function(request){
        var oldarticle=document .getElementById ("oldarticle");
        oldarticle.innerHTML=request .responseText;
    }
}

//上传图文
function send_arc(word,page_id){
	
    var cd=document.getElementById ("currentdiv");
    var title=document.getElementById("title").value;
    if(!cd||cd.style.width==""){
    alert("请选择图片选区");
    return false;
    }
    
    var divleft=cd.style.left;
    var divtop=cd.style.top;

    var http=new HTTPRequest();
    http.onresponse=function(request){
        if(request.responseText!=null){
            alert("上传成功");
		document.getElementById("sub").disabled = "";
            showarea(page_id);
            document.getElementById ("send_form").reset();
            FCKeditorAPI.GetInstance("content").EditorDocument.body.innerHTML = "";
            div=null;
        }
        else {alert("error");}
    }
    if(word=="new"){
    if(title==null||title==""){
            alert("请输入标题");
            return false;
        }
document.getElementById("sub").disabled = "disabled";
        http.send("action/arcticle.aspx","left="+divleft+"&top="+divtop+"&width="+cd.style.width+"&height="+cd.style.height+"&title="+encodeURIComponent(title)+"&sub_title="+encodeURIComponent(document.getElementById("sub_title").value)+"&reply_title="+encodeURIComponent(document.getElementById("reply_title").value)+"&author="+encodeURIComponent(document.getElementById("author").value)+"&keyword="+document.getElementById("Nkeyword").value+"&content="+encodeURIComponent(FCKeditorAPI.GetInstance("content").EditorDocument.body.innerHTML)+"&word="+encodeURIComponent(word)+"&page_id=" + page_id + "&show_author=" + document.getElementById("show_author").checked + "&pic_news=" + document.getElementById("pic_news").checked,"post");
    }
    else if(word=="old"){
        var oldart=document .getElementById ("oldart");
        if(oldart.options[oldart.selectedIndex].value=="0"){
            alert("请选择文章");
            return false;
        }
        http.send("action/arcticle.aspx","left="+divleft+"&top="+divtop+"&width="+cd.style.width+"&height="+cd.style.height+"&word_news_id="+oldart .options[oldart .selectedIndex].value+"&word="+encodeURIComponent(word)+"&page_id="+page_id,"post" );
    }
    else {alert("error");return false};
    
    return false;
}

//更新
function update_arc(word_news_id){
    var http=new HTTPRequest();
    http.onresponse=function(request){
        if(request .responseText=="ok"){
            alert("更新成功");
        }
        else{
            alert("error");
        }
    }
    http.send("action/update_arc.aspx","word_news_id="+word_news_id +"&title="+encodeURIComponent(document.getElementById ("Utitle").value)+"&sub_title="+encodeURIComponent(document.getElementById("Usub_title").value)+"&reply_title="+encodeURIComponent(document.getElementById("Ureply_title").value)+"&author="+encodeURIComponent(document.getElementById("Uauthor").value)+"&Ushow_author=" + document.getElementById("Ushow_author").checked + "&Upic_news=" + document.getElementById("Upic_news").checked + "&keyword="+document.getElementById("Ukeyword").value+"&content="+encodeURIComponent(FCKeditorAPI.GetInstance("Ucontent").EditorDocument.body.innerHTML),"post");
    
    return false;
}

//显示文章
//var isok1=true;
function showarticle(id){
//isok1=false;
if(isok==true){
    var http=new HTTPRequest();
    http.onresponse=function(request){
        var showarticle=document.getElementById("showarticle");
        showarticle.innerHTML=request.responseText;
        document.getElementById("edit").style.display="none";
        document.getElementById("showarticle").style.display="block";
        if(document.getElementById("Ucontent")) {
            var uContentEditor = new FCKeditor("Ucontent");
            uContentEditor.BasePath = "fckeditor/";
            uContentEditor.ToolbarSet = "Weekly";
            uContentEditor.Width = 600;
            uContentEditor.Height = 500;
            uContentEditor.ReplaceTextarea();
        }
    }
    http.send("action/showarticle.aspx","area_id=" + id , "post");
}
isok=true;
}

//矩形代码
var moveable=false ;
var againable=false ;
var picdiv=document.getElementById ("picdiv");
var div;


//down 函数
picdiv.onmousedown =function(e){
//    if(isok1 ==false){
//        isok1 = true;
//        return;
//    }
    e=e?e:event;
    var obj=e.srcElement?e.srcElement:e.target;
    if(obj!=picdiv){
        return;
    }
    change("new");
    var currentdiv=document.getElementById ("currentdiv");
    if(currentdiv&&obj==picdiv){
        var pd=currentdiv .parentNode ;
        pd.removeChild(currentdiv);
        corner.parentNode.removeChild(corner);
	div=null;
    }
    if(obj==corner||obj ==currentdiv){
        return;
    }
    div=document.createElement ("div");
    div.style.position="absolute";
    div.style.cursor="move";
    div.style.zIndex="20";
    div.id="currentdiv";
    div.onmousedown=divonmousedown;
    div.onmousemove=divonmousemove;
    div.onmouseout=div.onmouseup=divonmouseup;
    //div=document.getElementById("currentdiv");
    picdiv.appendChild (div);
    moveable=true;
    div.startPosition={clientX:e.clientX-10,clientY:e.clientY-80};
    div.style.left=div.startPosition.clientX + "px";
    div.style.top=(div.startPosition.clientY + document.documentElement.scrollTop) + "px";
    div.style.borderStyle="solid";
    div.style.borderWidth = "2px";
    div.style.display="none";
}

picdiv.onmousemove=function(e){
    if(moveable ==true){
        e=e?e:event;
        //var div=document.getElementById("currentdiv");
        div.style.display="block";
        div.style.width=(e.clientX-10 - div.startPosition.clientX) + "px";
        div.style.height=(e.clientY-80 - div.startPosition.clientY) + "px";
    }
}
//
var corner=document .createElement ("div");
picdiv.onmouseup=function(e){
    moveable = false ;
    //角落
    //var div=document.getElementById("currentdiv");
    picdiv.appendChild (corner);
    if(!div||div.style.height==""){corner.style.width="0px";corner.style.height="0px";return;}
    corner.style.position="absolute";
    corner .style.top=(parseInt(div.style.height)-15+parseInt(div.style.top))+"px";
    corner .style.left=(parseInt(div.style.width)-15+parseInt(div.style.left))+"px";
    //corner.style.borderStyle="solid";
    corner .style.height="15px";
    corner .style.width="15px";
    corner.style.zIndex="21";
    corner.id="corner";
    corner.style.cursor="se-resize";
}
corner.onmousedown=function(e){
    e=e?e:event;
    corner.startx=e.clientX-10;
    corner.starty=e.clientY-80;
    againable  =true; 
    div.startwidth=parseInt(div.style.width);
    div.startheight=parseInt(div.style.height);

}
corner.onmouseout=corner.onmouseup=function(){
    againable =false ;
   
}
corner.onmousemove=function(e){
    if(againable ==true){
        e=e?e:event;
        div.style.width=div.startwidth +e.clientX-10-corner .startx+"px";
        div.style.height=div.startheight +e.clientY-80-corner .starty+"px";
        corner.style.top=(parseInt(div.style.height)-15+parseInt(div.style.top))+"px";
        corner.style.left=(parseInt(div.style.width)-15+parseInt(div.style.left))+"px";
    }
}

//移动调整
var adjustable=false ;
//down函数
function divonmousedown(e){
    e = e?e:event;
    var obj=e.srcElement?e.srcElement:e.target;
    if(obj==corner){return;}
        div .movePosition={movex:e.clientX-10,movey:e.clientY-80};
        adjustable =true ;
        div.x=parseInt(div .style.left,10);
        div.y=parseInt(div .style.top,10);
}

function divonmousemove(e){
    if(adjustable ==true ){
        e = e ? e : event;
        div .style.left=e.clientX-10 -div .movePosition.movex  + div.x + "px";
        div .style.top=e.clientY-80 - div .movePosition.movey  + div.y + "px";
    }
}
function divonmouseup(){
    adjustable =false ;
}

var isok=true;
var isok1=true;
//删除area
function delarea(id,page_id){
var delword=0;
if(confirm("确认删除选区")){
    if(confirm("同时删除对应文字新闻吗？")){delword=1;}
    var http=new HTTPRequest();
    http.send("action/delarea.aspx?id="+id+"&word="+delword,"","post");
    http.onresponse=function(request){
        if(request.responseText=="ok"){
            showarea(page_id);
        }
        else {alert("error");}
    }
}
isok=false;
return false;
}



