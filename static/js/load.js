function GetPic(paras){
    var http = new HTTPRequest();
    if(paras == null){
        http.onresponse = function(request){
            showpic(request.responseText);
        }
        http.send("webajax/getpage_id.aspx");
    }
    else if(paras["word_news_id"]){
        http.onresponse = function(request){
            showpic(request.responseText,paras["word_news_id"]);
        }
        http.send("webajax/getpage_id.aspx?word_news_id=" + paras["word_news_id"]);
    }
    else if(paras["paper_id"]){
        var http = new HTTPRequest();
        http.onresponse = function(request){
            showpic(request.responseText);
        }
        http.send("webajax/getpage_id.aspx?paper_id=" + paras["paper_id"]);
    }
    else if(paras["page_id"]){
        showpic(paras["page_id"]);
    }
    else{
        http.onresponse = function(request){
            showpic(request.responseText);
        }
        http.send("webajax/getpage_id.aspx");
    }
}
//获取图片
function showpic(page_id,word_news_id){
    var http=new HTTPRequest();
    http.onresponse=function(request){
        var showpic=document .getElementById ("showpic");
        showpic.innerHTML=request.responseText;
    }
    http.send ("webajax/getimage.aspx?page_id=" + page_id + "&word_news_id=" + word_news_id,"","post");
}

function GetPageName(paras){
    var http = new HTTPRequest();
    if(paras == null){
        http.onresponse = function(request){
            var p = request.responseText.split(',');
            showpaper(p[0],p[1]);
        }
        http.send("webajax/GetPaperId.aspx");
    }
    else if(paras["word_news_id"]){
        http.onresponse = function(request){
            var p = request.responseText.split(',');
            showpaper(p[0],p[1]);
        }
        http.send("webajax/GetPaperId.aspx?word_news_id=" + paras["word_news_id"]);
    }
    else if(paras["paper_id"]){
        http.onresponse = function(request){
            showpaper(paras["paper_id"],request.responseText);
        }
        http.send("webajax/getpage_id.aspx?paper_id=" + paras["paper_id"]);
    }
    else if(paras["page_id"]){
        http.onresponse = function(request){
            var p =request.responseText.split(',');
            showpaper(p[0],p[1]);
        }
        http.send("webajax/GetPaperId.aspx?page_id=" + paras["page_id"]);
    }
    else{
        http.onresponse = function(request){
            var p = request.responseText.split(',');
            showpaper(p[0],p[1]);
        }
        http.send("webajax/GetPaperId.aspx");
    }
}

//获取版名
function showpaper(paper_id,page_id){
    var http=new HTTPRequest();
    http.onresponse=function(request){
        var pagename=document .getElementById ("pagename");
        pagename.innerHTML =request.responseText;
        ChangePaperName(paper_id);
    }
    http.send("webajax/getpagename.aspx?paper_id=" + paper_id + "&page_id=" + page_id,"","post")
}

function ChangePaperName(paper_id){
    var http = new HTTPRequest();
    http.onresponse = function(request){
        var span = document.getElementById("span");
        span.innerHTML = "第" + request.responseText + "期";
    }
    http.send("webajax/getpapername.aspx?paper_id=" + paper_id);
}

//文章、新闻list
function GetNews(paras){
    var http = new HTTPRequest();
    if(paras == null){
        http.onresponse = function(request){
            shownews(request.responseText);
        }
        http.send("webajax/getpage_id.aspx");
    }
    else if(paras["word_news_id"] && !paras["keyword"]){
        var http = new HTTPRequest();
        http.onresponse = function(request){
        showarticle(paras["word_news_id"],"page_id=" + request.responseText);
        }
        http.send("webajax/getpage_id.aspx?word_news_id=" + paras["word_news_id"]);
    }
    else if(paras["paper_id"]){
        var http =new HTTPRequest();
        http.onresponse = function(request){
            shownews(request.responseText);
        }
        http.send("webajax/getpage_id.aspx?paper_id=" + paras["paper_id"]);
    }
    else if(paras["word_news_id"] && paras["keyword"]){
        if(!paras["page"]){
            paras["page"] = "0";
        }
        showarticle(paras["word_news_id"],"keyword=" + paras["keyword"] + "&page=" + paras["page"]);
    }
    else if(paras["keyword"] && !paras["page"]){
        Paging("gopage","0",paras["keyword"]);
    }
    else if(paras["keyword"] && paras["page"]){
        Paging("gopage",paras["page"],paras["keyword"]);
    }
    else if(paras["page_id"]){
        shownews(paras["page_id"]);
    }
    else{
        http.onresponse = function(request){
            shownews(request.responseText);
        }
        http.send("webajax/getpage_id.aspx");
    }
}


function shownews(page_id){
    var news=document .getElementById("news");
    news.innerHTML = "<div style='height:500px'><p style='padding-top:50px;padding-left:50px'>加载中...</p></div>";
    var http=new HTTPRequest();
    http.onresponse=function(request){
        news.innerHTML=request.responseText;
        document.getElementById("newslist").style.display = 'block';
    }
    http.send ("webajax/getnews.aspx?page_id=" + page_id);
}

function showarticle(word_news_id,value){
    var news = document.getElementById("news");
    news.innerHTML = "<div style='height:500px'><p style='padding-top:50px;padding-left:50px'>加载中...</p></div>";
    var http=new HTTPRequest();
        http.onresponse=function(request1){

            news.innerHTML = request1.responseText;
        }
    http.send("webajax/showarticle.aspx?word_news_id=" + word_news_id + "&" + value,"","post");
    return false;
}

function Paging(word,page,keyword){
    var news=document .getElementById ("news");
    news.innerHTML = "<div style='height:500px'><p style='padding-top:50px;padding-left:50px'>加载中...</p></div>";
    var http=new HTTPRequest();
    http.onresponse=function(request){
        news.innerHTML =request.responseText;
	if(document.getElementById("newslist")){
            document.getElementById("newslist").style.display = 'block';
        }
    }
    if(word=="pre"){
        http.send ("webajax/search.aspx?page=" + (page-1) + "&keyword=" + keyword,"","post");
        window.location.href = "#keyword=" + keyword + "&page=" + (page-1) + "&gopage=true";
    }
    else if(word=="next"){
        page++;
        http.send("webajax/search.aspx?page=" + page + "&keyword=" + keyword,"","post");
        window.location.href = "#keyword=" + keyword + "&page=" + page + "&gopage=true";
    }
    else if(word=="gopage"){
        http.send("webajax/search.aspx?page=" + page + "&keyword=" + keyword,"","post");
        window.location.href = "#keyword=" + keyword + "&page=" + page + "&gopage=true";
    }
    return false;
}