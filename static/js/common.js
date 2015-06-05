/**
 * Created by ilovey on 6/1/15.
 */

// 用CKEditor替换<textarea id="editor1">
// 使用默认配置
var editor = CKEDITOR.replace('content', {
    height: 400
});

$(document).ready(function () {
    $("#submit").click(function () {
        var title = $("#title").val().trim();
        if (title == "") {
            alert("标题不能为空!");
            return false;
        }
        var replyTitle = $("#reply-title").val().trim();
        var subTitle = $("#sub-title").val().trim();
        var author = $("#author").val().trim();
        var content = editor.document.getBody().getHtml();
        if (content == "") {
            alert("正文内容不能为空!");
            return false;
        }
        var showAuthor = 0;
        var hasPic = 0;
        if ($("#show-author").is(":checked")) {
            showAuthor = 1;
        }
        if ($("#has-pic").is(":checked")) {
            hasPic = 1;
        }
        alert(title + replyTitle + subTitle + author + showAuthor + hasPic + content);
        return false;
    });





});

function changeArticle(article_id) {
    $(function () {
        $.get("/admin/article/" + article_id, function (data, status) {
            var jsonData = $.parseJSON(data);
            if (status == 'success' && jsonData.code == 1) {
                $("#title").val(jsonData.data.title);
                $("#author").val(jsonData.data.author);
                $("#sub-title").val(jsonData.data.sub_title);
                $("#reply-title").val(jsonData.data.reply_title);
                var isSelected = false;
                if (jsonData.data.show_author == 1) {
                    isSelected = true
                }
                $("#show-author").attr("checked", isSelected);
                if (jsonData.data.has_pic == 1) {
                    isSelected = true
                } else {
                    isSelected = false
                }
                $("#has-pic").attr("checked", isSelected);
                editor.document.getBody().setHtml(jsonData.data.content);
            }
        });
        return false;
    });
}