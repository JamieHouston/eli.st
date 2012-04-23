var elist = elist || {};
elist.UI = elist.UI || {};

(function ($) {
    (function() {
        this.initListView = function(){

            $('body').on('click', '#add_item', addItem);
            $newItem = $('#new_item');

            runOnEnter($newItem, addItem);

            $newItem.focus();
        };

        function runOnEnter($target, action){
            $target.on('keyup', function(e){
                if (e.keyCode == 13) action();
            });
        }

        function addItem(){
            var newItem = $('#new_item').val();
            $.ajax('add/' + newItem, {
                success: function(data){
                    item = JSON.parse(data);
                    $('#items').prepend('<label class="checkbox" data-order="' + item.order + '" id="item_' +
                        item.pk + '"><input type="checkbox" name="complete" id="' + item.pk + '"><span>' + item.name +
                        '</span><span class="tag" style="display:none;"><i class="icon-plus tag-action" id="new_{{ item.pk }}"></i>add tag</span><div class="item-actions"><i class="icon-trash delete-item" style="display:none;"></i><i class="icon-move move-item" style="display:none;"></i></div></label>');
                    $('#new_item').val('');
                }
            });
        }

    }).apply(elist.UI);
})(jQuery);
