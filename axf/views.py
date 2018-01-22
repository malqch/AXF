import hashlib

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from axf.models import Wheel, Nav, MustBuy, Shop, MainShow, FoodType, Goods, User, Cart, Order


def home(request):
    title = "主页"
    # 查询数据
    wheels = Wheel.objects.all()
    # 查询导航数据
    navs = Nav.objects.all()
    # 必购商品
    mustbuys = MustBuy.objects.all()
    # 查询便利商店
    shops = Shop.objects.all()
    shops_more = shops[3:7]
    shops_rec = shops[7:11]
    # 查询mainshow
    main_show = MainShow.objects.all()

    context = {"title": title,
               "wheels": wheels,
               "navs": navs,
               "mustbuys": mustbuys,
               "shops": shops,
               "shop_more": shops_more,
               "shops_rec": shops_rec,
               "main_show": main_show
               }

    return render(request, 'axf/home/home.html', context=context)


def market(request, typeid, childcid, sort_rule):
    title = "闪送超市"
    # 查询所有类型
    foodtypes = FoodType.objects.all()

    if childcid == '0':
        goods_list = Goods.objects.filter(categoryid=typeid)
    else:
        # 查询所以商品
        goods_list = Goods.objects.filter(categoryid=typeid).filter(childcid=childcid)

    # 销量升序
    if sort_rule == "1":
        goods_list = goods_list.order_by('productnum')
    # 销量降序
    elif sort_rule == "2":
        goods_list = goods_list.order_by('-productnum')
    # 价格降序
    elif sort_rule == "3":
        goods_list = goods_list.order_by('-price')
    # 价格升序
    elif sort_rule == "4":
        goods_list = goods_list.order_by('price')
    # 综合排序
    else:
        pass

    # 根据typeid将childtypenames拿出来
    foodtype = FoodType.objects.filter(typeid=typeid)

    # 创建一个默认值
    childtypenames = "全部分类：0"
    if len(foodtype) > 0:
        childtypenames = foodtype.first().childtypenames
    # 切割数据
    childtypenamelist = childtypenames.split("#")
    childtypenamelisttran = []

    print(childtypenamelist)
    # 二次处理数据
    # [["名称","id"],["名称","id"],["名称","id"],]
    for item in childtypenamelist:
        itemtran = item.split(":")
        childtypenamelisttran.append(itemtran)
    print(childtypenamelisttran)

    sort_rule_list = [["综合排序", "0"], ["销量升序", "1"], ["销量降序", "2"], ["价格最低", "3"], ["价格最高", "4"]]

    context = {
        "title": title,
        "foodtypes": foodtypes,
        "goods_list": goods_list[0:20],
        "childtypenamelist": childtypenamelisttran,
        "typeid": typeid,
        "childcid": childcid,
        "sort_rule_list": sort_rule_list,
    }
    return render(request, 'axf/market/market.html', context=context)


def mine(request):
    # 标题  title
    title = "个人中心"

    username = request.session.get("username")
    if username == None:
        username = "未登录"
        usericon = ''
        is_login = False
    else:
        is_login = True
        user = User.objects.get(u_name=username)
        # usericon = "http://127.0.0.1:8000/static/uploadfiles/" + user.u_icon.path
        usericon = "http://127.0.0.1:8026/static/uploadfiles/" + user.u_icon.url
        print(usericon)
    context = {
        "title": title,
        "is_login":is_login,
        "username":username,
        "usericon":usericon,
    }

    return render(request, 'axf/mine/mine.html', context=context)


def cart(request):
    title = "购物车"
    # 判断是否登陆
    username = request.session.get("username")
    if username == None:
        return redirect(reverse("axf:login"))
    # 已登录
    user = User.objects.get(u_name=username)
    carts = Cart.objects.filter(c_user=user).filter(c_belong=False)


    context = {
        "carts":carts,
        "title":title,
    }

    return render(request, 'axf/cart/cart.html',context=context)


def urlToMarket(request):
    return redirect(reverse("axf:market", args=["104749", "0", "0"]))

# 登陆界面
def login(request):
    return render(request,'axf/user/login.html')

# 注册界面
def register(request):
    return render(request,'axf/user/register.html')

# 执行注册
def doregister(request):
    # 存储用户信息
    try:
        username = request.POST.get('username')
        password =request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        icon = request.FILES['icon']
        print(password)

        # 获取摘要
        md5 = hashlib.md5()

        # 将原始数据进行摘要计算    原数据需要转换成二进制格式
        md5.update(password.encode("utf-8"))
        # 获取摘要后的信息  hex  16进制   digest获取二进制摘要输出
        # digest()获取的是二进制输出   hexdigest()  获取的是16进制输出，16进制可以直接转换成可见字符串
        p = md5.hexdigest()
        print(p)
        password = p


        user = User()
        user.u_name = username
        user.u_password = password
        user.u_emal = email
        user.u_phone = phone
        user.u_icon = icon

        user.save()
        # 将用户关键信息存储在session
        request.session['username'] = username
        return redirect(reverse('axf:mine'))
        # return HttpResponse("注册成功%d" % user.id)
    except Exception as e:
        print("注册失败")
        return HttpResponse("注册失败")

# 登出
def logout(request):
    # del request.session["username"]
    response = HttpResponseRedirect(reverse("axf:mine"))
    response.delete_cookie("sessionid")

    return response


def checkuser(request):
    uname = request.GET.get("uname")
    users = User.objects.filter(u_name=uname)

    if len(users) > 0:
        msg = "该用户名已存在,请重新输入"
        state = 201

    else:
        msg = "此用户名可用"
        state = 200

    data = {"msg":msg,"state":state}
    return  JsonResponse(data)

"""
    使用摘要算法
        hashlib
            md5
            sha
"""


def dologin(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    """
        两种写法
            直接去数据库查询用户名和密码
            用用户名查找，没找到提示用户名不存在
            用户名找到了再去验证密码
    """
    user = User.objects.filter(u_name=username)
    print(user.first().u_name)

    if len(user) > 0:
    #     比对密码  将密码进行hash算法后进行比较
        md5 = hashlib.md5()
        md5.update(password.encode("utf-8"))
        newpassword = md5.hexdigest()
        if newpassword == user.first().u_password:
            request.session["username"] = username
    #         登陆成功   跳转回个人中心
            response = HttpResponseRedirect(reverse("axf:mine"))
            return response
        else:
            return redirect(reverse("axf:login"))
    else:
        return redirect(reverse("axf:login"))


def userinfomod(request):
    title = "个人信息修改"

    username = request.session.get("username")
    uname = User.objects.get(u_name=username)
    password = uname.u_password
    context = {
        "title":title,
        "username":username,
        "password":password,
    }
    return render(request,'axf/user/userinfomod.html',context=context)


def douserinfomod(request):
    # 获取相关信息
    username = request.session.get("username")
    uname = User.objects.get(u_name=username)

    icon = request.FILES['icon']
    email = request.POST.get('email')
    phone = request.POST.get('phone')

    uname.u_icon = icon
    uname.u_emal = email
    uname.u_phone = phone

    uname.save()

    return redirect(reverse("axf:mine"))



def addtocart(request):
    # 判断用户是否登陆
    username = request.session.get("username")
    if username == None:
        return JsonResponse({"msg":"您还没有登录，请先登录"})
        # return redirect(reverse("axf:login"))

    # 用户已登录  添加到购物车
    goods_id = request.GET.get("goodsid")
    goods = Goods.objects.get(pk=goods_id)
    # 获取登陆用户信息
    user = User.objects.get(u_name=username)
    # 先去数据库查找
    c = Cart.objects.filter(c_user=user).filter(c_goods=goods).filter(c_belong=False)
    if len(c) == 0:
        c = Cart()
    else:
        c = c.first()
        num = c.c_goods_num
        c.c_goods_num = num+1

    # 存储购物信息

    c.c_user = user
    c.c_goods = goods

    c.save()
    return JsonResponse({"msg":"添加成功"})


def changeselect(request):
    cartid = request.GET.get("cartid")
    cartselected = request.GET.get("cartselected")

    print(cartid)
    print(cartselected)

    car = Cart.objects.get(pk=cartid)
    if cartselected == "True":
        car.c_select = False
    else:
        car.c_select = True

    car.save()
    return JsonResponse({"msg":"ok"})


def cartgoodssub(request):
    cartid = request.GET.get("cartid")
    # print(cartid)
    car = Cart.objects.get(pk=cartid)
    num = car.c_goods_num
    if num == 1:
    #     删除此条数据
        car.delete()
    else:
        car.c_goods_num = num - 1
        car.save()
    return JsonResponse({"num":num - 1,"msg":"ok"})


def cartgoodsadd(request):
    cartid = request.GET.get("cartid")
    car = Cart.objects.get(pk=cartid)
    num = car.c_goods_num
    car.c_goods_num = num + 1
    car.save()
    return JsonResponse({"num":num + 1})


def genorder(request):
    cartids = request.GET.get("cartids")
    cartids = cartids.split("#")
    print(cartids)
    # 生成订单  将要购买的商品转换到订单表中   将要购买的商品订单关联
    order = Order()
    username = request.session.get("username")
    user = User.objects.get(u_name=username)

    order.o_user = user
    # 定义状态  0默认状态   1 已下单未付款  2 已付款 .....
    order.o_status = 1
    order.save()
    # order 存储之后就有id了
    # 购物车数据更新
    for item in cartids:
        car = Cart.objects.get(pk=item)
    #     修改属于哪张表
        car.c_belong = True
        car.c_order = order
        car.save()

    return JsonResponse({"msg":"ok","orderid":order.id})

# 支付，相关平台注册开发者账号，配置自己的信息，     ping++可以快速集成多种支付
def pay(request,orderid):

    context = {
        "orderid":orderid,
    }
    return render(request,'axf/order/pay.html',context=context)


