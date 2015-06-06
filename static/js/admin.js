/**
 * Created by ilovey on 6/5/15.
 */

$(document).ready(function () {
    /*******复选框渲染**********/
    if ($('[data-toggle="switch"]').length) {
        $('[data-toggle="switch"]').bootstrapSwitch();
    }

    $('input[type="checkbox"]').click(function () {
        alert("ok");
        // Do something
    });

    $(".update").click(function () {
        var $pa = $(this).parent();
        $pa.css("display", "none");
        $pa.next().css("display", "block");
    });

    $(".cancel").click(function () {
        var $li = $(this).parents("li");
        $li.find(".item-hidden").css("display", "none");
        $li.find(".item-show").css("display", "block");
    });

    $(".save").click(function () {
        var $pageNum = $(this).siblings(".page-num-value");
        var $pageName = $(this).siblings(".page-name-value");
        ;
        var pageId = $(this).data("pageId");
        var $li = $(this).parents("li");
        $.post("/admin/updatePage", {
            page_id: pageId,
            page_num: $pageNum.val(),
            page_name: $pageName.val()
        }, function (data, status) {
            if (status == "success") {
                var json = $.parseJSON(data);
                if (json.code == 1) {
                    alert(json.data);
                    $li.find(".item-hidden").css("display", "none");
                    $li.find(".item-show").css("display", "block");
                    $li.find(".item-show span").text($pageNum.val() + "版:" + $pageName.val());
                    $li.find(".update").data("pageNum", $pageNum.val());
                    $li.find(".update").date("pageName", $pageName.val());
                } else {
                    alert(json.data);
                }
            }
        });
    });

    $(".delete-paper").click(function () {
        var paperNum = $(this).data("id");
        var isDelete = window.confirm("确定要删除第" + paperNum + "期期刊吗?");
        var $parent_li = $(this).parents("li");
        if (isDelete) {
            $.post("/admin/paper/delete", {
                paper_num: paperNum
            }, function (data, status) {
                if (status == "success") {
                    var json = $.parseJSON(data);
                    alert(json.data);
                    if (json.code == 1) {
                        $parent_li.remove();
                    }
                } else {
                    alert("网络连接错误!");
                }
            });
            return false;
        }
        return false;
    });

    /*****报刊删除****/
    $(".delete-page").click(function(){
        var isDeleted = window.confirm("确定要删除这版报刊吗?");
        if (! isDeleted) return false;
        var $parent = $(this).parents(".page-edit-item");
        var pageId = $parent.data("id");
        $.post("/admin/deletePage", {
            page_id: pageId
        }, function (data, status) {
            if(status == "success"){
                var json = $.parseJSON(data);
                alert(json.data);
                if(json.code ==1 ){
                    $parent.remove();
                }
            }else{
                alert("网络连接失败");
            }
        });
    });


    $(".edit-page").click(function(){
        var pageId = $(this).parents(".page-edit-item").data("id");
        window.location.href= "http://" + window.location.host + "/admin/edit/page/" + pageId;
    });
});