$(function(){
        $(document).ready(function(){
				$('#datepicker').datetimepicker({
				 format: 'yyyy-mm-dd',
				 autoclose: true,
				 todayHighlight: true,
				 minuteStep: 2,
				 todayBtn: true,
				 pickDate: true,
				 pickTime: false
				});
			});
	
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

});
