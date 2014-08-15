var storage = localStorage;
var consts = {
    K_CLASSES_REFRESH: 'event:classes:refresh',  // 刷新分类列表
    K_ARTICLE_REFRESH: 'event:article:refresh'  // 刷新某篇文章
};


$(function(){
    // === 左侧导航栏 === //
    $('.submenu > a').click(function(e){
        e.preventDefault();
        var submenu = $(this).siblings('ul');
        var li = $(this).parents('li');
        var submenus = $('#sidebar li.submenu ul');
        var submenus_parents = $('#sidebar li.submenu');
        var w = $(window).width();
        if(li.hasClass('open')){
            if((w > 768) || (w < 479)){
                submenu.slideUp();
            }else{
                submenu.fadeOut(250);
            }
            li.removeClass('open');
        }else{
            if((w > 768) || (w < 479)){
                submenus.slideUp();
                submenu.slideDown();
            }else{
                submenus.fadeOut(250);
                submenu.fadeIn(250);
            }
            submenus_parents.removeClass('open');
            li.addClass('open');
        }
    });

    var ul = $('#sidebar > ul');

    $('#sidebar > a').click(function(e){
        e.preventDefault();
        var sidebar = $('#sidebar');
        if(sidebar.hasClass('open')){
            sidebar.removeClass('open');
            ul.slideUp(250);
        }else{
            sidebar.addClass('open');
            ul.slideDown(250);
        }
    });


    // === 改变窗口大小 === //
    $(window).resize(function(){
        if($(window).width() > 479){
            ul.css({'display':'block'});
            $('#content-header .btn-group').css({width:'auto'});
        }
        if($(window).width() < 479){
            ul.css({'display':'none'});
            fix_position();
        }
        if($(window).width() > 768){
            $('#user-nav > ul').css({width:'auto',margin:'0'});
            $('#content-header .btn-group').css({width:'auto'});
        }
    });

    if($(window).width() < 468){
        ul.css({'display':'none'});
        fix_position();
    }
    if($(window).width() > 479){
       $('#content-header .btn-group').css({width:'auto'});
        ul.css({'display':'block'});
    }

    // ajax加载之后的title不能正常显示出来
    function tooltip(){
        $('.tip').tooltip();
        $('.tip-left').tooltip({placement: 'left'});
        $('.tip-right').tooltip({placement: 'right'});
        $('.tip-top').tooltip({placement: 'top'});
        $('.tip-bottom').tooltip({placement: 'bottom'});
    }
    tooltip();


    // === ajax事件完成之后重新渲染title === //
    $(document).ajaxComplete(function(){
        tooltip();
    });

    // === 输入提示 === //
    $('#search input[type=text]').typeahead({
        source: ['Dashboard','Form elements','Common Elements','Validation','Wizard','Buttons','Icons','Interface elements','Support','Calendar','Gallery','Reports','Charts','Graphs','Widgets'],
        items: 4
    });

    // === 修复content header和右上角的按钮组位置 === //
    function fix_position(){
        var uwidth = $('#user-nav > ul').width();
        $('#user-nav > ul').css({width:uwidth,'margin-left':'-' + uwidth / 2 + 'px'});

        var cwidth = $('#content-header .btn-group').width();
        $('#content-header .btn-group').css({width:cwidth,'margin-left':'-' + uwidth / 2 + 'px'});
    }
});


// 显示消息通知
function notify(text, image){
    var opt = {
        title: '提示(' + now_str() + ')',
        text: text,
        sticky: false
    };
    if(typeof image !== 'undefined'){
        opt.image = image;
    }
    $.gritter.add(opt);
    return false;
}


// 当前日期时间的字符串(2013-04-05 06:07:08)
function now_str(){
    var dt = new Date(),
        y = dt.getFullYear(),
        m = dt.getMonth() + 1,
        d = dt.getDate(),
        h = dt.getHours(),
        M = dt.getMinutes(),
        s = dt.getSeconds();
    m = m > 9 ? m : '0' + m;
    d = d > 9 ? d : '0' + d;
    h = h > 9 ? h : '0' + h;
    M = M > 9 ? M : '0' + M;
    s = s > 9 ? s : '0' + s;
    return y + '-' + m + '-' + d + ' ' + h + ':' + M + ':' + s;
}


// 是否正在提交
function is_submiting(btn){
    return $(btn).data('block') === 'blocked';
}


// 阻塞提交
function block_submit(btn){
    var $btn = $(btn);
    $btn.data({block: 'blocked', val: $btn.val()}).addClass('disabled').val('稍等片刻...');
}


// 释放按钮
function unblock_submit(btn){
    var $btn = $(btn);
    $btn.data('block', null).removeClass('disabled').val($btn.data('val'));
}


// 表单验证
function form_validate(form, rules, on_submit){
    var $form = $(form);
    $form.validate({
        rules: rules,
        errorClass: 'help-inline',
        errorElement: 'span',
        highlight: function(e){
            $(e).parents('.control-group:first').addClass('error');
        },
        unhighlight: function(e){
            $(e).parents('.control-group:first').removeClass('error');
        },
        submitHandler: function(){
            on_submit($form);
        }
    });
}
