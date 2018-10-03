function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(function () {

    $(".base_info").submit(function (e) {
        e.preventDefault()

        var signature = $("#signature").val()
        var username = $("#username").val()
        var gender = $(".gender").val()

        if (!username) {
            alert('请输入昵称')
            return
        }
        if (!gender) {
            alert('请选择性别')
        }

        // TODO 修改用户信息接口
         var params = {
            "signature": signature,
            "username": username,
            "gender": gender
        }
        $.ajax({
            url: "/user/base_info",
            type: "post",
            contentType: "application/json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            data: JSON.stringify(params),
            success:function (resp) {
                if (resp.errno == "0") {
                    // 更新父窗口内容
                    $('.user_center_name', parent.document).html(params['username'])
                    $('#username', parent.document).html(params['username'])
                    $('.input_sub').blur()
                }else {
                    alert(resp.errmsg)
                }

            }
        })
    })
})