from django.conf.urls import url

from axf import views

urlpatterns = [
    url(r'^home/',views.home,name='home'),
    url(r'^mine/',views.mine,name='mine'),
    url(r'^market/$',views.urlToMarket,name='urltomarket'),
    url(r'^market/(\d+)/(\d+)/(\d+)',views.market,name='market'),
    url(r'^cart/',views.cart,name='cart'),
    url(r'^mine/',views.mine,name='mine'),
    url(r'^login/',views.login,name='login'),
    url(r'^dologin/',views.dologin,name='dologin'),
    url(r'^register/',views.register,name='register'),
    url(r'^doregister/',views.doregister,name='doregister'),
    url(r'^logout/',views.logout,name='logout'),
    url(r'^checkuser/',views.checkuser,name='checkuser'),
    url(r'^userinfomod/',views.userinfomod,name='userinfomod'),
    url(r'^douserinfomod/',views.douserinfomod,name='douserinfomod'),
    url(r'^addtocart/',views.addtocart,name='addtucart'),
    url(r'^changeselect/',views.changeselect,name='changeselect'),
    url(r'^cartgoodssub/',views.cartgoodssub,name='cartgoodssub'),
    url(r'^cartgoodsadd/',views.cartgoodsadd,name='cartgoodsadd'),
    url(r'^genorder/',views.genorder,name='genorder'),
    url(r'^pay/(\d+)',views.pay,name='pay'),
]