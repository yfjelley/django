$(function(){
    	$('#bt100').click(function(){
           $('#com').load('/rank/',{'feature':$("#feature").val(),'keywords':$("#keywords").val()},
            function(){
                      alter('xxx');
                });
            });
});
