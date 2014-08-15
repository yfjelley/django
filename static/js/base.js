$(function(){
$(document).ready(function(){
        $("#dd").datebox({
                  required: "true",
                  missingMessage: "请输入日期",
                  formatter: function (date) {
                      var y = date.getFullYear();
                      var m = date.getMonth() + 1;
                      var d = date.getDate();
                      return y + "-" + (m < 10 ? ("0" + m) : m) + "-" + (d < 10 ? ("0" + d) : d) + "";
                  }
              });
		$("#b04").click(function(){
			var time = $("#dd").datebox("getValue");
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


})
