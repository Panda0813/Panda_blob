tinyMCE.init({
    "theme": "advanced",
    "mode": "textareas",
    "width": 800,
    "height": 600
});


function save() {

    console.log(n);

}

//模态框提示发布成功
function submit() {
    $('#saveModal').modal({backdrop: 'static', show: true});
    var content = tinyMCE.activeEditor.getContent();
    setTimeout(function () {
        $.ajax('/user/blob', {
            type: 'post',
            data: $('form').serialize()+'&content='+encodeURIComponent(content),
            dataType: 'json',
            success: function (data) {
                if (data.status == 'ok') {
                    $('#saveMsg').text(data.msg);
                    setTimeout(function () {
                        $('#saveModal').modal('hide');
                        window.open('/user/blob?a=1', target = '_self')
                    }, 1500)
                }
            }
        })
    }, 2000)
}


// 判断信息是否未填
$(function () {
    $('#save').click(function () {
        var ipts = document.getElementsByTagName('input');
        var n = 0;
        console.log(ipts);
        for (var i in ipts) {
            var ipt = ipts[i];
            console.log(ipt);
            if (ipt.value == "") {
                ipt.placeholder = "信息不能为空";
                n++;
            }
        }
        if (n == 1 || n == 0) {
            submit();
        }

    })
})