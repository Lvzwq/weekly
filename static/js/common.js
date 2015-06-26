/**
 * Created by ilovey on 6/1/15.
 */

// 用CKEditor替换<textarea id="content">
// 使用默认配置
var editor = CKEDITOR.replace('content', {
    height: 400
});

$("select").select2({dropdownCssClass: 'dropdown-inverse'});


$(document).ready(function () {
    //将表单中的内容清空
    function resetContent(){
        $("#title").val("");
        editor.document.getBody().setHtml("");
        $("#reply-title").val("");
        $("#sub-title").val("");
        $("#author").val("");
        $("#has-pic").attr("checked", false);
        $("#show-author").attr("checked", false);
    }


    $("#submit").click(function () {
        var title = $("#title").val().trim();
        var content = editor.document.getBody().getHtml();
        if (title == "") {
            alert("标题不能为空!");
            return false;
        }
        if (content == "") {
            alert("正文内容不能为空!");
            return false;
        }
        var replyTitle = $("#reply-title").val().trim();
        var subTitle = $("#sub-title").val().trim();
        var author = $("#author").val().trim();
        var pageId = $("#select-pic").data("id");   // 获得pageId

        var showAuthor = 0;
        var hasPic = 0;
        if ($("#show-author").is(":checked")) {
            showAuthor = 1;
        }
        if ($("#has-pic").is(":checked")) {
            hasPic = 1;
        }
        var $right = $(".right");
        var isNew = $right.data("isNew");
        var isSubmit;

        if (isNew == "1") {
            //新增一篇文章
            isSubmit = window.confirm("确认提交这篇文章吗?");
            if (isSubmit) {
                var x = $right.data("x");
                var y = $right.data("y");
                var width = $right.data("width");
                var height = $right.data("height");
                $.post("/admin/article", {
                    x: x,
                    y: y,
                    width: width,
                    height: height,
                    title: title,
                    reply_title: replyTitle,
                    sub_title: subTitle,
                    author: author,
                    show_author: showAuthor,
                    has_pic: hasPic,
                    content: content,
                    page_id: pageId
                }, function (data) {
                    var json = $.parseJSON(data);
                    if (json.code == 1) {
                        alert("提交成功");
                        var articleId = json.data.id;
                        var html = addArea(x, y, width, height, articleId);
                        $("#select-pic").append(html);
                        return false;
                    }
                    alert(json.data);
                });
            }
            return false;
        } else {
            //修改一篇文章
            var articleId = $(".right").data("id");
            if (!articleId) {
                alert("请选择左侧区域或者截图确认截图");
                return false;
            }
            isSubmit = window.confirm("确认修改这篇文章吗?");
            if (isSubmit) {
                $.post("/admin/article/" + articleId, {
                    title: title,
                    reply_title: replyTitle,
                    sub_title: subTitle,
                    author: author,
                    show_author: showAuthor,
                    has_pic: hasPic,
                    content: content,
                    page_id: pageId
                }, function (data) {
                    var json = $.parseJSON(data);
                    alert(json.data);
                    return false;
                });
            }
            return false;
        }
    });

    //定义报刊截图区
    var jcrop_api;
    //开启截图
    $('#scrop-on').click(function (e) {
        $('.page-pic').Jcrop({}, function () {
            jcrop_api = this;
        });
        jcrop_api.enable();
        return false;
    });

    //禁用截图
    $('#scrop-off').click(function (e) {
        var $jcropHolder = $(".jcrop-holder");
        if ($jcropHolder.length == 0) {
            alert("已经处于禁用状态");
            return false;
        }
        jcrop_api.release();
        var $showPic = $("#showpic");
        $("#select-pic").appendTo($showPic);
        $jcropHolder.remove();
        $(".right").removeAttr("data-is-new");
        $showPic.append('<div class="page-pic"></div>');
        $("#select-pic").appendTo($(".page-pic"));
        return false;
    });

    //提交截图
    $('#scrop-submit').click(function (e) {
        if (!jcrop_api) {
            alert("请先截图，再提交!");
            return false;
        }
        var scale = jcrop_api.tellSelect();
        var $right = $(".right");
        $right.attr("data-x", scale.x);
        $right.attr("data-y", scale.y);
        $right.attr("data-width", scale.w);
        $right.attr("data-height", scale.h);
        $right.attr("data-is-new", 1);
    });

    //重置的点击动作
    $("#reset").click(function () {
        resetContent();
        return false;
    });

    //添加新一版按钮点击动作
    $("#add-page").click(function(){
        var pageId = $(".right").data("pageId");
        window.location.href = "http://" + window.location.host + "/admin/add_page/" + pageId;
        return false;
    });


    //本期已有文章
    $("#paper-article").click(function () {
        var pageId = $(".right").data("pageId");
        var $articleList = $("#article-list");
        var display = $articleList.css("display");
        $articleList.toggle();
        $("form").toggle();
        if (display == "block"){
            $(this).text("本期已有文章");
        }else{
            $(this).text("发布新文章");
        }
        var id = $("select option:eq(0)").data("id");
        if(id == pageId) return false;
        $.get("/admin/paper/article?page_id=" + pageId, {}, function (data) {
            var json = $.parseJSON(data);
            var $select = $("select");
            $.each(json.data, function(){
                $select.append('<option value="' + this[0] + '" >'+ this[1] +'</option>');
            });
            $("select option:eq(0)").attr("data-id", pageId);
        });
        return false;
    });


    //select文章时的动作事件
    $("#article-title").change(function(){

    });

    //确定按钮
    $("#insure").click(function(){
        var id = $("select option:selected").val();
        var title = $("select option:selected").text();
        alert(id + title);
    });

});

function changeArticle(article_id) {
    $(function () {
        var display = $("#article-list").css("display");
        if(display == "block"){
            $("#div" + article_id).css("border", "1px solid black");
            return false;
        }
        $.get("/admin/article/" + article_id, function (data, status) {
            var jsonData = $.parseJSON(data);
            if (status == 'success' && jsonData.code == 1) {
                $("#title").val(jsonData.data.title);
                $("#author").val(jsonData.data.author);
                $("#sub-title").val(jsonData.data.sub_title);
                $("#reply-title").val(jsonData.data.reply_title);
                var isSelected = false;
                if (jsonData.data.show_author == 1) {
                    isSelected = true;
                }
                $("#show-author").attr("checked", isSelected);
                if (jsonData.data.has_pic == 1) {
                    isSelected = true;
                } else {
                    isSelected = false;
                }
                $("#has-pic").attr("checked", isSelected);
                editor.document.getBody().setHtml(jsonData.data.content);
            }
        });
        var $right = $(".right");
        $right.attr("data-id", article_id);
        $right.removeAttr("data-is-new");
        return false;
    });
}


function addArea(x, y, width, height, id) {
    return '<div style="position: absolute; top: ' + y + 'px; left: ' + x + 'px;" id="div' + id + '"> <div><img src="/static/images/tip.gif"></div></div><div class="area-item"' +
        'style="left: ' + x + 'px; top: ' + y + 'px; width: ' + width + 'px; height: ' + height + 'px;"onclick="changeArticle(' + id + ');">;</div>';
}

function deleteArea(area_id){
    alert(area_id);
}

