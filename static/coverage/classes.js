$(function(){
    	$('#bt100').click(function(){
				 $('table').load('/day/',{'date':time,'department':$("#dep").val(),'site':$("#site").val(),'media':$("#med").val(),'addres':$("#add").val()},
                     )};
            )};
);
