$(function(){
    	$('#bt1000').click(function(){
           $('#com').load('/commit/',{'feature':$("#feature").val(),'keywords':$("#keywords").val()});
            });
});
