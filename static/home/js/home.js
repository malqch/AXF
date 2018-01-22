$(function () {

    //   加载完成   延迟
    setTimeout(function () {
        topSwiper();
        swiperMenu();
    },1000)

})

function topSwiper() {
    var topSwiper = new Swiper("#topSwiper",{
        loop:true,
        autoplay:4000,
        pagination: '.swiper-pagination',
    })
}

function swiperMenu() {
    var topSwiper = new Swiper("#swiperMenu",{
        slidesPerView: 3,

    })
}
