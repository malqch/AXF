$(function () {
    // 类型过滤
    $("#all_type").click(function () {
        // alert("quanbuleix")
        $("#all_type_content").css("display", "block").click(function () {
            $(this).css("display", "none");

            // $("#all_type_content").click(function () {
            //     $(this).css("display","none")
        })
    })
    // 结果集排序规则
    $("#sort_rule").click(function () {
        $("#sort_rule_content").css("display", "block").click(function () {
            $(this).css("display", "none");

        })
    })
//    商品加购物车
    $(".goods_add").click(function () {
        // alert("剁手了")
    //    将商品数据发送到服务器   添加到购物车   将商品id发送到服务器

        var goodsid = $(this).attr("goods_id");
        // alert(goodsid);
        // 写地址的时候，浏览器上写的是ip就写ip   使用的是域名就写域名
        $.get("http://127.0.0.1:8026/axf/addtocart/",{"goodsid":goodsid},function (data) {
            // alert(data["msg"]);
            if(data["msg"] == "您还没有登录，请先登录"){
                alert(data["msg"])
                window.open("http://127.0.0.1:8026/axf/login/","_self");
            }else {
                    alert(data["msg"])
                }
        })
    })

})