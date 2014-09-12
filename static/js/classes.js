$(function(){
	    function page_tables(){
			var $table = $('table.classes');
			$table.dataTable({
				'bJQueryUI': true,
				'sPaginationType': 'full_numbers',
				'sDom': '<""l>t<"F"fp>',
				'bDestroy': true,
				'bInfo': true,
				'bAutoWidth':false,
				"oLanguage":{
				'sProcessing' : "正在加载...",
				'sLengthMenu' : "每页显示_MENU_条记录",
				'sZeroRecords' : "对不起,查询不到相关数据！",
				'sEmptyTable' : "表中无数据存在！",
				'sInfo' : "当前显示_START_到_END_条，共_TOTAL_条记录",
				'sInfoFiltered' : "数据表中共为_MAX_条记录",}
			});
			$table.css('width','100%');
		};
		page_tables()
    	$('#b04').click(function(){
				 var time = $("#datepicker").val()||'all';
				 $('table').load('/day/',{'date':time,'department':$("#dep").val(),'site':$("#site").val(),'media':$("#med").val(),'addres':$("#add").val()},
					function(){
							 page_tables();
							 }
		 );
     	});
    	$('#b01').click(function(){
				 var time = $("#week").val()||'all';
				 $('table').load('/week/',{'date':time,'department':$("#dep").val(),'site':$("#site").val(),'media':$("#med").val(),'addres':$("#add").val()},
				function(){
						 page_tables();
						 }
		 );
		});
});
