$(function () {
    rightSwiper();  //轮播图

    $('a[name="deleteBlob"]').click(function () {
        id = this.title;
        $('#deleteModal').modal({backdrop:'static',show:true});
        $('#ok').click(function () {
            $.ajax('/user/blob?delete_id='+id,{
            type:'delete',
            dataType:'json',
            success:function (data) {
                if(data.status == 'ok'){
                    console.log(data.msg);
                    $('#delMsg').text(data.msg);
                    $('.modal-footer').css('display','none');
                    setTimeout(function () {
                        $('#deleteModal').modal('hide');
                        window.open('/user/blob?a=1',target='_self')
                    },1500)
                }
            }
        })
        })

    })

});

//右侧轮播图
function rightSwiper() {
    var swiper = new Swiper('#topSwiper',{
        direction:'horizontal',
        loop:true,  //让slide是循环的
        pagination:'.swiper-pagination',
        paginationClickable:true,
        autoplay:2000,  //自动播放
        autoplayDisableOnInteraction:false  //用户触动以后可以继续使用autoplay
        // delay:3000
    })
}