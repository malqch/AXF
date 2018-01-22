$(function () {
//  获取选项按钮
    $(".ischose").click(function () {
    //  将当前点击的选项的id发送给服务器
        var cart_id = $(this).attr("cartid");
        var cart_selected = $(this).attr("cartselected");
        var child = $(this).find("span");
        if(cart_selected == "True"){
            $(this).attr("cartselected","False");
        }else{
            $(this).attr("cartselected","True");
        }

        $.getJSON("http://127.0.0.1:8026/axf/changeselect/",{"cartid":cart_id,"cartselected":cart_selected},function (data) {
            if(data["msg"] == "ok"){
                $(child).toggle();
            }
        })
    })
    //  购物车-按钮
    $(".subShopping").click(function () {
        // alert("减1")
    //    获取到点击的id
        var sub = $(this);
        var cartid = sub.attr("cartid");
    //    将信息传递给服务器
        $.getJSON("http://127.0.0.1:8026/axf/cartgoodssub/",{"cartid":cartid},function (data) {
            // alert(data["num"])
            if(data["num"] == 0){
            //    删除此条数据
                sub.parents("li").remove();
            }else{
            //    就是将num放到显示区域
                sub.next("span").html(data["num"]);
            }
        })
    })

//    购物车+按钮
    $(".addShopping").click(function () {
    //    获取点击到的id
        var sub = $(this);
        var cartid = sub.attr("cartid");
    //    将信息传递给服务器
        $.getJSON("http://127.0.0.1:8026/axf/cartgoodsadd/",{"cartid":cartid},function (data) {
            sub.prev("span").html(data["num"]);
        })
    })

//  添加下单点击
    $("#select_ok").click(function () {
    //    获取所以包含数据的item,内部为显示的获取出来
        var spans = $(".ischose").find("span");
        var cartids = [];
        for (var i = 0; i < spans.length;i++){
            if($(spans[i]).css("display") == "block"){
                console.log($(spans[i]).attr("id"));
                cartids.push($(spans[i]).attr("id"));
            }
        }
        console.log(cartids);
        $.getJSON("http://127.0.0.1:8026/axf/genorder/",{"cartids":cartids.join("#")},function (data) {
            alert(data["msg"]);
        //    接收到订单id,拿着id进行页面跳转，去付款
            window.open("http://127.0.0.1:8026/axf/pay/"+data["orderid"],"_self");
        })
    })
})