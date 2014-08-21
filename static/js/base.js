$(function(){
$(document).ready(function(){
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
		
				
        $('.ns-dtpicker').datetimepicker({
     	 format: 'yyyy-mm-dd  ',
         autoclose: true,
	     todayHighlight: true,
	      minuteStep: 2,
	     todayBtn: true
	    });
			});


});
