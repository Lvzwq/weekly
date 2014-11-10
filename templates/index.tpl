<!DOCTYPE html>

<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

    <title>华中科技大学校报</title>

    <link href="/assets/css/index.css" rel="stylesheet" type="text/css">
    <script type="text/javascript" src="/assets/js/http_request.js"></script>
    <script type="text/javascript" src="/assets/js/url.js"></script>
    <script type="text/javascript" src="/assets/js/load.js"></script>
    <script type="text/javascript" src="/assets/js/index.js"></script>
</head>

<body onload="FirstLoad()">
    <div class="head">
        <div class="head1">
            <ul>
                <li style="background-image: none"><a href="http://weekly.hustnews.com/index/#" onclick="return HomePage.call(this);">
                    设为主页</a></li>
                <li><a href="http://weekly.hustnews.com/index/#" onclick="return Love();">加入收藏</a></li>
            </ul>
        </div>
        <div class="nouse">
            <img src="/assets/images/bar2.jpg">
        </div>
        <div class="head3">
            <pre>中共华中科技大学委员会主办 国内统一刊号：CN-0802/（G）</pre>
            <img src="/assets/images/logo.png">
        </div>
    </div>
    <div style="clear: both">
    </div>
    <div class="left">
        <div class="select">
            <select class="s" id="select1" name="Select1" onchange="changepaper(this.options[this.selectedIndex].value)">
                <option value="0">----请选择期数----</option>

                {% for paper in papers %}
                    <option value="{{paper.id}}" qs="第{{paper.num}}期">
                        {{paper.date}} "第{{paper.num}}期"
                    </option>
                {% endfor %}

            </select>
            <pre>总{{latest_num}}期 当前期数：<span id="span">第{{latest_num}}期</span></pre>
        </div>
        <div class="baozhi" id="showpic">


<div style="
background: url(http://images.hustnews.com/weekly/2014/11/1004.jpg);
background-repeat: no-repeat;
position: relative;
width: 409px;
height: 597px;
">

<div style="width:100%;height:100%;background: url(assets/image/banner.gif) no-repeat;"></div>


 {% for area in areas %}
                      <div style="position: absolute; display: none; top: {{area.title_y}}; left: {{area.x}}; z-index: 22; font-size: 12px; width: {{area.width}};" id="div{{area.article_id}}">
<div style="margin-left:15px"><img src="image/tip.gif"></div>
<div style="background-color: #eb545d;color:#45070b; padding:8px;text-align:center;">
        <span style="font-size:14px;font-weight:bold">{{area.title}}</span>
</div>
    </div>
    <div style="cursor: pointer; position: absolute; left: {area.x}; top: {area.y}; width: {area.width}; height: {area.height};"
    onmouseover="this.style.border='red 2px solid';document.getElementById('div{area.article_id}').style.display='block';"
    onmouseout="this.style.border='';;document.getElementById('div{{area.article_id}}').style.display='none';" onclick="window.location.href='/article/{area.article_id}';FirstLoad()">
    </div>
                {% endfor %}





      <div style="position: absolute; display: none; top: 401px; left: 21px; z-index: 22; font-size: 12px; width: 210px;" id="div7393">
<div style="margin-left:15px"><img src="image/tip.gif"></div>
<div style="background-color: #eb545d;color:#45070b; padding:8px;text-align:center;">
        <span style="font-size:14px;font-weight:bold">校党委中心组专题学习加强意识形态工作</span>
</div>
    </div>
    <div style="cursor: pointer; position: absolute; left: 21px; top: 227px; width: 92px; height: 167px;" onmouseover="this.style.border='red 2px solid';document.getElementById('div7393').style.display='block';" onmouseout="this.style.border='';;document.getElementById('div7393').style.display='none';" onclick="window.location.href='#word_news_id=7393';FirstLoad()">
    </div>



      <div style="position: absolute; display: none; top: 560px;
        left: 22px;z-index:22;font-size:12px;width:210px" id="div7394">
<div style="margin-left:15px"><img src="image/tip.gif"></div>
<div style="background-color: #eb545d;color:#45070b; padding:8px;text-align:center;">
        <span style="font-size:14px;font-weight:bold">我校与法德高校拓展合作</span>
</div>
    </div>
    <div style="cursor: pointer; position: absolute; left: 22px                                              ; top: 401px                                             ;
        width: 93px                                              ; height: 152px                                             ;" onmouseover="this.style.border='red 2px solid';document.getElementById('div7394').style.display='block';" onmouseout="this.style.border='';;document.getElementById('div7394').style.display='none';" onclick="window.location.href='#word_news_id=7394';FirstLoad()">
    </div>



      <div style="position: absolute; display: none; top: 556px; left: 120px; z-index: 22; font-size: 12px; width: 210px;" id="div7395">
<div style="margin-left:15px"><img src="image/tip.gif"></div>
<div style="background-color: #eb545d;color:#45070b; padding:8px;text-align:center;">
        <span style="font-size:14px;font-weight:bold">六学者获张培刚发展经济学优秀成果奖</span><br>2014中国经济发展论坛同时举行
</div>
    </div>
    <div style="cursor: pointer; position: absolute; left: 120px; top: 404px; width: 256px; height: 145px;" onmouseover="this.style.border='red 2px solid';document.getElementById('div7395').style.display='block';" onmouseout="this.style.border='';;document.getElementById('div7395').style.display='none';" onclick="window.location.href='#word_news_id=7395';FirstLoad()">
    </div>



      <div style="position: absolute; display: none; top: 397px; left: 293px; z-index: 22; font-size: 12px; width: 210px;" id="div7396">
<div style="margin-left:15px"><img src="image/tip.gif"></div>
<div style="background-color: #eb545d;color:#45070b; padding:8px;text-align:center;">
        <span style="font-size:14px;font-weight:bold">校友曹林张彦武何桂香分获中国新闻奖一等奖</span>
</div>
    </div>
    <div style="cursor: pointer; position: absolute; left: 293px; top: 283px; width: 88px; height: 107px;" onmouseover="this.style.border='red 2px solid';document.getElementById('div7396').style.display='block';" onmouseout="this.style.border='';;document.getElementById('div7396').style.display='none';" onclick="window.location.href='#word_news_id=7396';FirstLoad()">
    </div>



      <div style="position: absolute; display: none; top: 285px; left: 292px; z-index: 22; font-size: 12px; width: 210px;" id="div7397">
<div style="margin-left:15px"><img src="image/tip.gif"></div>
<div style="background-color: #eb545d;color:#45070b; padding:8px;text-align:center;">
        第七届企业家论坛暨第二届创业投融资论坛举行<br><span style="font-size:14px;font-weight:bold">校友热议新常态新机遇</span>
</div>
    </div>
    <div style="cursor: pointer; position: absolute; left: 292px; top: 100px; width: 90px; height: 178px;" onmouseover="this.style.border='red 2px solid';document.getElementById('div7397').style.display='block';" onmouseout="this.style.border='';;document.getElementById('div7397').style.display='none';" onclick="window.location.href='#word_news_id=7397';FirstLoad()">
    </div>



      <div style="position: absolute; display: none; top: 398px; left: 120px; z-index: 22; font-size: 12px; width: 210px;" id="div7398">
<div style="margin-left:15px"><img src="image/tip.gif"></div>
<div style="background-color: #eb545d;color:#45070b; padding:8px;text-align:center;">
        <span style="font-size:14px;font-weight:bold">奏响十月华章</span>
</div>
    </div>
    <div style="cursor: pointer; position: absolute; left: 120px; top: 228px; width: 163px; height: 163px;" onmouseover="this.style.border='red 2px solid';document.getElementById('div7398').style.display='block';" onmouseout="this.style.border='';;document.getElementById('div7398').style.display='none';" onclick="window.location.href='#word_news_id=7398';FirstLoad()">
    </div>

</div>

</div>
    </div>
    <div class="right" id="righttext">
        <form action="" onsubmit="return KeySearch();" class="search">
        <div class="fdj">
            <img src="./华中科技大学校报_files/fdj.png"></div>
        <div>
            <input class="Checkbox1" type="text" id="keyword"></div>
        <div class="ss" style="cursor: pointer">
            <input type="image" src="./华中科技大学校报_files/ss.png"></div>
        <div class="dqrq">
            <pre>当前日期：2014年11月9日  星期日</pre>
        </div>
        <div style="clear: both">
        </div>
        </form>
        <div class="text">
            <div class="yumen">
                <div class="bmdh">
                    <p>
                        版面导航</p>
                </div>
                <div class="arrowleft" id="scrollleft" onmouseover="pagemove(&#39;left&#39;)" onmouseout="delmove()" style="cursor: pointer;">
                    <img src="./华中科技大学校报_files/aleft.png">
                </div>
                <div class="B" style="float: left; width: 300px; position: relative; overflow: hidden" id="pagename">

<div style="position: absolute; width: 280px; left: -1px" id="namelist">
    <ul>

        <li style="width: 65px; margin-left: 3px;text-align:center; overflow: hidden;"><a href="http://weekly.hustnews.com/index/#" onclick="window.location.href=&#39;#page_id=1004&#39;;FirstLoad();return false;">
            <span style="color:#FFFD00">要闻</span></a></li>

        <li style="width: 65px; margin-left: 3px;text-align:center; overflow: hidden;"><a href="http://weekly.hustnews.com/index/#" onclick="window.location.href=&#39;#page_id=1005&#39;;FirstLoad();return false;">
            <span style="">综合</span></a></li>

        <li style="width: 65px; margin-left: 3px;text-align:center; overflow: hidden;"><a href="http://weekly.hustnews.com/index/#" onclick="window.location.href=&#39;#page_id=1006&#39;;FirstLoad();return false;">
            <span style="">视点</span></a></li>

        <li style="width: 65px; margin-left: 3px;text-align:center; overflow: hidden;"><a href="http://weekly.hustnews.com/index/#" onclick="window.location.href=&#39;#page_id=1007&#39;;FirstLoad();return false;">
            <span style="">副刊</span></a></li>

    </ul>
</div>
</div>
                <div class="arrowright" style="cursor: pointer" onmouseover="pagemove(&#39;right&#39;)" onmouseout="delmove()">
                    <img src="./华中科技大学校报_files/aright.png">
                </div>
            </div>
            <div>
                <div id="loading" style="width: 80px; margin-left: 50px; margin-top: 50px; display: none;
                    height: 380px">
                    加载中...</div>
                <div id="news">
<div id="newslist" class="C" style="height: 500px; overflow-y: auto; display: block;">
    <ul class="content">

        <li><a href="http://weekly.hustnews.com/index/#" onclick="window.location.href=&#39;#word_news_id=7392&#39;;FirstLoad();return false; ">
            脉冲强磁场实验装置跻身世界“最好”</a><!--a href="" onclick="changepaper('273','第508期')">2014年11月3日第508期</a--></li>

        <li><a href="http://weekly.hustnews.com/index/#" onclick="window.location.href=&#39;#word_news_id=7393&#39;;FirstLoad();return false; ">
            校党委中心组专题学习加强意识形态工作</a><!--a href="" onclick="changepaper('273','第508期')">2014年11月3日第508期</a--></li>

        <li><a href="http://weekly.hustnews.com/index/#" onclick="window.location.href=&#39;#word_news_id=7394&#39;;FirstLoad();return false; ">
            我校与法德高校拓展合作</a><!--a href="" onclick="changepaper('273','第508期')">2014年11月3日第508期</a--></li>

        <li><a href="http://weekly.hustnews.com/index/#" onclick="window.location.href=&#39;#word_news_id=7395&#39;;FirstLoad();return false; ">
            六学者获张培刚发展经济学优秀成果奖</a><!--a href="" onclick="changepaper('273','第508期')">2014年11月3日第508期</a--></li>

        <li><a href="http://weekly.hustnews.com/index/#" onclick="window.location.href=&#39;#word_news_id=7396&#39;;FirstLoad();return false; ">
            校友曹林张彦武何桂香分获中国新闻奖一等奖</a><!--a href="" onclick="changepaper('273','第508期')">2014年11月3日第508期</a--></li>

        <li><a href="http://weekly.hustnews.com/index/#" onclick="window.location.href=&#39;#word_news_id=7397&#39;;FirstLoad();return false; ">
            校友热议新常态新机遇</a><!--a href="" onclick="changepaper('273','第508期')">2014年11月3日第508期</a--></li>

        <li><a href="http://weekly.hustnews.com/index/#" onclick="window.location.href=&#39;#word_news_id=7398&#39;;FirstLoad();return false; ">
            奏响十月华章[<span style="color: Red">图</span>]</a><!--a href="" onclick="changepaper('273','第508期')">2014年11月3日第508期</a--></li>

    </ul>
</div>
</div>
            </div>
        </div>
        <!--div class="editors" id="rightfoot">
            <h1>
                欢迎投稿</h1>
            <h2>
                您可以通过E-mail或电话</h2>
            <img src="image/envelope.png"></img>
            <div class="E">
                <div class="E1">
                    <h3>
                        校报编辑部</h3>
                    <p>
                        xbbjb@mail.hust.edu.cn</p>
                </div>
                <div class="E2">
                    <h4>
                        校报主编<span>&nbsp;胡艳华</span></h4>
                    <p>
                        yanhuahu@mail.hust.edu.cn</p>
                </div>
                <div class="E3">
                    <h5>
                        校报副主编<span>&nbsp;万霞</span></h5>
                    <p>
                        wanxia76@mail.hust.edu.cn</p>
                </div>
            </div>
            <div class="NO">
                <h3>
                    热线电话：027-87542701</h3>
                <h3>
                    传真电话：027-87541544</h3>
            </div>
        </div-->
    </div>
    <div style="clear: both;">
    </div>
    <div class="tail">
        <pre>华中科技大学校报编辑部出版  邮箱：xbbjb@mail.hust.edu.cn  电话：027-87542701  传真：027-87541544
地址：华中科技大学新闻中心四楼  邮编：430074
版权所有©1999-2008    <a href="http://www.bingyan.net/" target="_blank">冰岩作坊</a> 制作维护</pre>
    </div>


</body></html>