$(function () {

    $("#register_username").blur(function () {
    //    失去焦点，获取输入框中的内容，需要将输入框中的内容发送给服务器去验证
        var uname = $(this).val()
        //  向服务器发送用户名进行验证
        $.getJSON("http://127.0.0.1:8026/axf/checkuser/",{"uname":uname},function (data) {
            // alert(data["msg"]);
            if(data["state"] == 200){
                 $("#username_check").css("color","#00ff00");
            }else if (data["state"] == 201){
                $("#username_check").css("color","#ff0000");
            }
            $("#username_check").html(data["msg"])
        })
    })

})

function check() {
    // alert("恶意注册")
    // return false
    //  做提交前的验证

    //  验证密码和确认密码
    var pwd = $("#register_password").val()
    var pwdc = $("#register_password_confirm").val()
    if(pwd == pwdc){
        // alert("一致")
        $("#password_check").html("两次密码一致");
        $("#password_check").css("color","#00ff00");
    }else{
        // alert("不一致")
        $("#password_check").html("两次密码不一致");
        $("#password_check").css("color","#ff0000");
        return false;
    }

    var newPwd = md5(pwd);
    $("#register_password").val(newPwd);


    return true;
}
