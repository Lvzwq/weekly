/**
 * Created by ilovey on 6/5/15.
 */

$(document).ready(function () {

    $('[data-toggle="switch"]').click(function () {
        alert("ok");
    });

    /*******复选框渲染**********/
    if ($('[data-toggle="switch"]').length) {
        $('[data-toggle="switch"]').bootstrapSwitch();
    }

    //点击发布switchChange.bootstrapSwitch
    $('input[type="checkbox"]').on('switchChange.bootstrapSwitch', function (event, state) {
        var issued = state ? 1 : 0;
        var paperId = $(this).attr("id").substr(7);
        $.get("/admin/paper/issued/"+ issued, {
            paper_id: paperId
        }, function(data, status){
            if(status == 'success'){
                var jData = $.parseJSON(data);
                alert(jData.data);
            }
            return false;
        });
        //if ($(this).is(":checked")) {
        //    var result = confirm("确认发布这一期报刊吗?");
        //    alert("你点击了" + result);
        //    if (result) {
        //        issued = 1;
        //    } else {
        //        $(this).bootstrapSwitch("setState", false);
        //        //$(this).prop('checked', true);
        //        return false;
        //    }
        //} else {
        //    var result = confirm("确认不发布这一期报刊吗");
        //    if (!result) {
        //        //$(this).checked(true);
        //        //$(this).prop('checked', true);
        //        return false;
        //    }
        //}
    });


    //$('input[type="checkbox"]').bootstrapSwitch('onColor', 'primary');
    //$('input[type="checkbox"]').bootstrapSwitch('offColor', 'danger');


    /***修改按钮动作****/
    $(".update").click(function () {
        var $pa = $(this).parent();
        $pa.css("display", "none");
        $pa.next().css("display", "block");
    });

    /****取消动作*****/
    $(".cancel").click(function () {
        var $li = $(this).parents("li");
        $li.find(".item-hidden").css("display", "none");
        $li.find(".item-show").css("display", "block");
    });

    /******保存按钮*******/
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

    /******左侧删除期刊******/
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
    $(".delete-page").click(function () {
        var isDeleted = window.confirm("确定要删除这版报刊吗?");
        if (!isDeleted) return false;
        var $parent = $(this).parents(".page-edit-item");
        var pageId = $parent.data("id");
        $.post("/admin/deletePage", {
            page_id: pageId
        }, function (data, status) {
            if (status == "success") {
                var json = $.parseJSON(data);
                alert(json.data);
                if (json.code == 1) {
                    $parent.remove();
                }
            } else {
                alert("网络连接失败");
            }
        });
    });


    /******点击后台首页编辑按钮跳转****/
    $(".edit-page").click(function () {
        var pageId = $(this).parents(".page-edit-item").data("id");
        window.location.href = "http://" + window.location.host + "/admin/edit/page/" + pageId;
    });
});