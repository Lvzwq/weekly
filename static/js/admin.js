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
        $pa = $(this).parent();
        $pa.css("display", "none");
        $pa.next().css("display", "block");
    });

    $(".cancel").click(function () {
        $li = $(this).parents("li");
        $li.find(".item-hidden").css("display", "none");
        $li.find(".item-show").css("display", "block");
    });

    $(".save").click(function () {
        var pageNum = $(this).siblings(".page-num-value").val();
        var pageName = $(this).siblings(".page-name-value").val();
        alert(pageName + pageNum);
    });

    $(".delete-paper").click(function () {
            var paperId = $(this).data("id");
            var isDelete = window.confirm("确定要删除第"+ paperId +"期期刊吗?");
            var $parent_li = $(this).parents("li");
            if (isDelete) {
                $.post("/admin/paper/delete", {
                    paper_id: paperId
                }, function(data, status){
                    if(status == "success"){
                        var json = $.parseJSON(data);
                        alert(json.data);
                        if(json.code == 1){
                            $parent_li.remove();
                        }
                    }else{
                        alert("网络连接错误!");
                    }
                });
                return false;
            }
            return;
        }
    )
    ;
});