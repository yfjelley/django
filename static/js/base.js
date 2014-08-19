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
		$("#b04").click(function(){
			var time = $("#datepicker").val();
			if(time == ""){
				alert("请选择日期！");
			};
			var JSONObject={'date':time,'department':$("#dep").val(),'site':$("#site").val(),'media':$("#med").val(),'addres':$("#add").val()};
			htmlobj=$.ajax({
				type:"post",
				url:"../../test1/",
				data:JSONObject,
               success:function(data){
			$("#myDiv").html(htmlobj.responseText);
			console.log(htmlobj);
			}
			});
			});
			});


});
