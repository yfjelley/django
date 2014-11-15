$(function(){
    	$('#bt1000').click(function(){
           $('#com').load('/com/',{'feature':$("#feature").val(),'keywords':$("#keywords").val()},
            function(){
                      alter('xxx');
                });
            });
});
