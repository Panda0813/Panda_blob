tinyMCE.init({
    "theme": "advanced",
    "mode": "textareas",
    "width": 789,
    "height": 200
});

$(function () {
    $('#save').click(function () {
        var blob_id = $('input[name="blob_id"]').val();
        var content = tinyMCE.activeEditor.getContent();  //提取富文本内容
        console.log(content);
        $.ajax('/user/replay', {
            type: 'post',
            data: {blob_id:blob_id,content:content},
            dataType: 'json',
            success: function (data) {
                //用户未登录
                if (data.status == 'fail') {
                    $('#replayMsg').text(data.msg);
                    $('#replayModal').modal({backdrop: 'static', show: true});
                    $('#ok').click(function () {
                        window.open('/user/login', target = '_self')
                    })
                } else if (data.status == 'ok') {  //已登录的用户
                    $('#replayMsg').text(data.msg);
                    $('#replayModal').modal({backdrop: 'static', show: true});
                    $('.modal-footer').css('display', 'none');
                    setTimeout(function () {
                        $('#replayModal').modal('hide');
                        blob_id = $('input[name="blob_id"]').val();
                        window.open('/user/show/' + blob_id, target = '_self')
                    }, 800)
                }
            }
        })
    })
});

//是iframe的高度随内容的变化而调整
function changeHeight() {
    var ifm = document.getElementById('frame');
    ifm.height = document.documentElement.clientHeight;
}

window.onResize = function () {
    changeHeight()
}