function changePaper(paper_id) {
    if (paper_id == "0") {
        return;
    }
    window.location.href = "/paper/" + paper_id;
}


$(document).ready(function () {
    //登录界面
    $("#login-button").click(function () {
        var uid = $("#login-name").val().trim();
        var pwd = $("#login-pass").val().trim();
        var $message = $(".message");
        if (uid == "" || pwd == "") {
            $message.text("name or password should not be empty!");
            $message.css("display", "block");
            return false;
        }
        $.post("/admin/login", {
            uid: uid,
            pwd: pwd
        }, function (data, status) {
            console.log(status);
            if (status == "success" && data.code == 1) {
                window.location.href = "/admin/index";
            } else if (data.code == -1) {
                $message.css("display", "block");
                $message.text(data.data);
            } else {
                $message.text("网络链接失败!");
                $message.css("display", "block");
            }
        }, "json");
        return false;
    });


    var r = /^[0-9]*[1-9][0-9]*$/;

    $(".add-paper button").click(function () {
        var paperNum = $("#paper-num").val().trim();
        var pubTime = $("#pub-time").val().trim();
        if (paperNum == "" || pubTime == "") {
            alert("期数和发布时间不能为空!");
            return false;
        }
        if (!r.test(paperNum)) {
            alert("期数应该是一个正整数");
            return false;
        }

        $.post("/admin/add_paper", {
            paper_num: paperNum,
            pub_time: pubTime
        }, function (data, status) {
            var jsonData = $.parseJSON(data);
            if (jsonData.code == -1) {
                alert(jsonData.data);
                return false;
            }
            if (jsonData.code == 1 && status == "success") {
                $(".current-paper,.add-page").removeClass("is-add");
                $(".add-paper, .add-file, .jump-paper").addClass("is-add");
                $(".pages").css("display", "block");
                $(".label-paper-num").text(paperNum);
                $(".label-pub-time").text(pubTime);
                var url = "http://" + window.location.host + "/admin/add_paper?paper_num=" + paperNum;
                history.pushState({}, "发布新期刊", url);
                return false;
            }
            alert("网络连接失败!");
            return false;
        });
    });

    /***重新修改期刊信息***/
    $(".current-paper button").click(function () {
        $(".pages").css("display", "none");
        $(".current-paper, .add-page").addClass("is-add");
        $(".add-paper, .jump-paper").removeClass("is-add");
        $("#paper-num").val($(".label-paper-num").text());
        $("#pub-time").val($(".label-pub-time").text());
        return false;
    });


    /****文件上传*****/
    $("#inputFile").uploadify({
        'swf': '/static/uploadify/uploadify.swf',
        'uploader': '/admin/image/upload?paper_num=' + $.trim($(".label-paper-num").text()),
        'formData': {'page_num': '', 'name': '', "page_id": ""},
        // Your options here
        'onUploadStart': function (file) {
            var pageNum = $('.label-num').text();
            var pageName = $('.label-name').text();
            var pageId = $(".add-file").attr("data-id");
            $("#inputFile").uploadify("settings", "formData", {
                'page_num': pageNum,
                'page_name': pageName,
                "page_id": pageId
            });
        },
        'onUploadSuccess': function (file, data, response) {
            console.log(file);
            if(response){
                var json = $.parseJSON(data);
                if (json.code == 1){

                }
                alert(json.data);
            }else{
                alert("网络连接失败!");
            }
        }
    });


    $('#inputFile').uploadify('settings', 'buttonText', '上传图片');

    $(".add-page button").click(function () {
        var pageNum = $.trim($("#adding-page-num").val());
        var pageName = $.trim($("#adding-page-name").val());
        if (pageNum == "" || pageName == "") {
            alert("版数和名称不能为空");
            return false;
        }
        if (!r.test(pageNum)) {
            alert("版数应该是一个正整数");
            return false;
        }
        $(".add-file").removeClass("is-add");
        $(".add-page").addClass("is-add");
        $(".label-num").text(pageNum);
        $(".label-name").text(pageName);
    });

    /*****修改报刊****/
    $(".add-file button").click(function () {
        var pageNum = $(".label-num").text();
        var pageName = $(".label-name").text();
        $(".add-file").addClass("is-add");
        $(".add-page").removeClass("is-add");
        $("#adding-page-num").val(pageNum);
        $("#adding-page-name").val(pageName);
    });

    /***跳转期刊***/
    $(".jump-paper button").click(function () {
        var paperNum = $.trim($(".jump-paper-num").val());
        if (paperNum == "") {
            alert("请填写跳转的期数");
            return false;
        }
        if (!r.test(paperNum)) {
            alert("请输入合法的期刊数");
            return false;
        }
        window.location.href = "http://" + window.location.host + "/admin/add_paper?paper_num=" + paperNum;
    });


    /***编辑期刊中报刊****/
    $(".pages button").click(function () {
        var $page = $(this).siblings(".page-item");
        var name = $page.data("name");
        var num = $page.data("num");
        var id = $page.data("id");
        $(".add-page").addClass("is-add");
        $(".add-file").removeClass("is-add");
        $(".label-num").text(num);
        $(".label-name").text(name);
        $(".add-file").attr("data-id", id);
    });


    /****首页删除按钮*****/
    $(".delete-paper").click(function () {
        alert("ok");
        var paperId = $(this).data("id");
        alert(paperId);
    });


});