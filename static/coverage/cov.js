$(function(){
    	$('#bt100').click(function(){
                var params={'feature':$("#feature").val(),'keywords':$("#keywords").val()};
                window.location.href='/jump?'+$.param(params);
            });
});
