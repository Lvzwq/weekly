function FirstLoad(){
    var url = document.location.href;
    var paras = new Array();
    paras = GetUrl(url);
    GetPic(paras);
    GetNews(paras);
    GetPageName(paras);
}

function changepaper(paper_id){
    if(paper_id == "0"){return;}
    window.location.href = "#paper_id=" + paper_id;
    FirstLoad();
}


function KeySearch(word){
    var http=new HTTPRequest();
    http.onresponse=function(request){
        var news=document .getElementById ("news");
        news.innerHTML = request.responseText;
	if(document.getElementById("newslist")){
        	document.getElementById("newslist").style.display = 'block';
	}
    }
    var keyword=document.getElementById ("keyword");
    if(word){
        http.send("webajax/search.aspx?keyword=" + escape(word));
    }
    else{
        if(keyword.value == ""){
            alert("请输入关键词");
            return false;
        }
        http.send("webajax/search.aspx?keyword="+escape(keyword .value));
        window.location.href = "#keyword=" + escape(keyword.value);
    }
    return false;
}



function Marquee(word){
    var namelist=document.getElementById("namelist");
    var width=namelist.offsetWidth;
    if(width<300){
        clearInterval(marq);
        return;
    }
    if(word=="right"&&parseInt(namelist.style.left)>-(width-301)){
        namelist.style.left=(parseInt(namelist.style.left)-1)+"px";
    }

    else if(word=="left"&&parseInt(namelist.style.left)<-1){
        namelist.style.left=(parseInt(namelist.style.left)+1)+"px";
    }
    else{clearInterval(marq);}
}

var marq;
function pagemove(word){
    var namelist=document.getElementById("namelist");
    marq=setInterval(function(){Marquee(word)},20);
}

function delmove(){
    clearInterval(marq);
}

function RightFoot(word){
    /*var rightfoot=document .getElementById ("rightfoot");
    if(word=="yes"){
        rightfoot .style.display ="block";
    }
    else{
        rightfoot.style .display ="none";
    }*/
}
//判断浏览器是否是ie
var isIE = navigator.userAgent.indexOf("MSIE") > 0;
var isFF = navigator.userAgent.indexOf("Firefox") > 0;
//主页
function HomePage(){
    if(isIE){
        this.style.behavior='url(#default#homepage)';this.setHomePage('http://weekly.hustnews.com');
    }
    return false;
}

//收藏
function Love(){
    if(isIE){
        window.external.AddFavorite('http://weekly.hustnews.com','校报电子版');
    }
    if(isFF){
        alert("你的浏览器是Firefox，收藏可按 Ctrl + D");
    }
    return false;
}

function Loading(word){
	var loading=document.getElementById("loading");
	if(word=="yes"){
		loading.style.display="block";
	}
	else{
		loading.style.display="none";
	}
}