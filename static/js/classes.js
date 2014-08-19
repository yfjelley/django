$(function(){

    // 生成表格
    function page_tables(){
        var $table = $('table.classes');
        $table.dataTable({
            'bJQueryUI': true,
            'sPaginationType': 'full_numbers',
            'sDom': '<""l>t<"F"fp>',
            'bDestroy': true
        });
        $table.css('width', '100%');  // dataTable重新生成表格后会变成165px
//        $('select').select2({width: 65});
    };
    page_tables();
    // 刷新表格
    $('#refresh').click(function(){
        $('table.classes').load('/admin.get.classes.json', function(){
            page_tables();
        });
    });

    // 删除分类
    $(document).on('click', 'table a.del', function(){
        var self = $(this);
        var $tr = self.parents('tr:first');
        var name = $tr.find('td:eq(1)').text();
        if(confirm('确认删除分类[ ' + name + ' ]吗?')){
            $.post('/admin.del.cls.json', {id: $tr.data('id')}, function(jsn){
                var msg;
                if(!jsn.err){
                    $('#refresh').click();
                    msg = '分类[ ' + name + ' ]已删除';
                    // 通知其他窗口更新分类列表
                    storage[consts.K_CLASSES_REFRESH] = Math.random();
                }else{
                    msg = jsn.msg;
                }
                notify(msg);
            });
        }
    });
    $(document).on('click', 'table a.rename', function(){
        var self = $(this);
        var $tr = self.parents('tr:first');
        var $td = $tr.find('td:eq(1)');
        var $input = $td.find('input');
        if($input.length != 0){
            $input.focus().select();
            return fasle;
        }
        var orign = $td.text();
        var $html = $('<input type="text" value="' + $td.text() + '"><br><a class="btn btn-mini ok"><i class="icon-ok"></i></a> <a class="cancel btn btn-mini"><i class="icon-remove"></i></a>');
        $td.empty().html($html);
        $input = $('input', $td).focus().select();
        $('.ok', $td).click(function(){
            $.post('/admin.rename.cls.json',
                   {id: $tr.data('id'), 'new': $input.val()}, function(jsn){
                       var msg;
                       if(jsn.err){
                           $input.focus().select();
                           msg = jsn.msg;
                       }else{
                           $td.text($input.val());
                           msg = '修改成功';
                       }
                       notify(msg);
            });
        });
        $('.cancel', $td).click(function(){
            $td.text(orign);
        });
    });
});
