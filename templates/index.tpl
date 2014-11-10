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
<body onload="showpic('{{page_id}}');showpaper('{{firstpaper}}');shownews('{{page_id}}')">
    <div class="head">
        <div class="head1">
            <ul>
                <li style="background-image: none"><a href="#" onclick="return HomePage.call(this);">
                    设为主页</a></li>
                <li><a href="#" onclick="return Love();">加入收藏</a></li>
            </ul>
        </div>
        <div class="nouse">
            <img src="image/bar2.jpg" />
        </div>
        <div class="head3">
            <pre>中共华中科技大学委员会主办 国内统一刊号：CN-0802/（G）</pre>
            <img src="image/logo.png" />
        </div>
    </div>
    <div style="clear: both">
    </div>
    <div class="left">
        <div class="select">
            <select class="s" id="select1" name="Select1" onchange="changepaper(this.options[this.selectedIndex].value,this.options[this.selectedIndex].getAttribute('qs'))">
                <option value="0">----请选择期数----</option>
                <%foreach (string[] str in paper)
                  {%>
                <option value="<%=str[0] %>" qs="第<%=str[1] %>期">
                    <%=str[2] %>
                    第<%=str[1] %>期</option>
                <%} %>
            </select>
            <pre>总<%=paper[0][1] %>期 当前期数：<span id="span">第<%=currentpaper %>期</span></pre>
        </div>
        <div class="baozhi" id="showpic">
        </div>
    </div>
    <div class="right" id="righttext">
        <form action="" onsubmit="return KeySearch();" class="search">
        <div class="fdj">
            <img src="image/fdj.png" /></div>
        <div>
            <input class="Checkbox1" type="text" id="keyword" /></div>
        <div class="ss" style="cursor: pointer">
            <input type="image" src="image/ss.png" /></div>
        <div class="dqrq">
            <pre>当前日期：<%=timenow %></pre>
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
                <div class="arrowleft" id="scrollleft" onmouseover="pagemove('left')" onmouseout="delmove()"
                    style="cursor: pointer;">
                    <img src="image/aleft.png" />
                </div>
                <div class="B" style="float: left; width: 300px; position: relative; overflow: hidden"
                    id="pagename">
                </div>
                <div class="arrowright" style="cursor: pointer" onmouseover="pagemove('right')" onmouseout="delmove()">
                    <img src="image/aright.png" />
                </div>
            </div>
            <div>
		<div id="loading" style="width:80px;margin-left:50px;margin-top:50px;display:none;height:380px">加载中...</div>
		<div id="news"></div>
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
版权所有&copy;1999-2008    <a href="http://www.bingyan.net/" target="_blank">冰岩作坊</a> 制作维护</pre>
    </div>
</body>
</html>
