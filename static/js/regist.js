function showError(msg) {
    var errorP = this.nextElementSibling;
    errorP.innerText = msg?msg:$(errorP).text();
    $(errorP).fadeIn();
    $(this).addClass('has-error');

    $(this).focus(function () {
        $(errorP).fadeOut();
        $(this).removeClass('has-error')
    })
}

$(function () {
    $('input').blur(function () {
        if(this.name == 'username'){
            name = this.value.trim();
            if(name.length == ''){
                showError.call(this,'用户名不能为空');
                return
            }
            $.getJSON('/user/uname/'+name+'/',function (data) {
                if(data.status == 'fail'){
                    showError.call($('input[name="username"]')[0],data.msg);
                    return
                }
            });
        }

        if(this.name == 'name' && this.value.trim() == ''){
            showError.call(this,false);
            return
        }


        if(this.name == 'phone'){
            phone = this.value.trim();
            if(phone.length == ''){
                showError.call(this,'手机号不能为空');
                return
            }
            if(!/1[3-9]\d{9}/.test(phone)){
                showError.call(this,'手机号无效');
                return
            }
        }

        if(this.name == 'passwd' && this.value.trim() == ''){
            showError.call(this,'密码不能为空');
            return
        }

        if(this.name == 'vcode'){
            vcode = this.value.trim();
            if(vcode.length == ''){
                showError.call(this,'');
                return
            }
        }

    });

});

function submitJudge() {
    var inputs = $('input');
    for(var i=1;i<inputs.length;i++){
        var input = inputs[i];
        if($(input).val().trim() == ''){
            showError.call(input,false);
            return
        }
    }
    vcode = $('input[name="vcode"]').val();
    if(vcode == undefined){
        document.forms[0].submit();
    }else {
        $.getJSON('/user/verify/'+vcode+'/',function (data) {
            if(data.status == 'fail'){
                showError.call($('#vcode')[0],data.msg);
                return
            }
            else{
                 document.forms[0].submit();
            }
        });
    }


}