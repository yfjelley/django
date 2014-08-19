$(function(){
        var $table = $('table.classes');
        $table.dataTable({
            'bJQueryUI': true,
            'sPaginationType': 'full_numbers',
            'sDom': '<""l>t<"F"fp>',
            'bDestroy': true
        });
});
