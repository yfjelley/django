$(function(){
    	$('#b100').click(function(){
				 $('table').load('/weekAccount/',{'date':time,'department':$("#dep").val(),'site':$("#site").val(),'media':$("#med").val()},
				function(){
						 page_tables();
						 }
		 );
		});
});
