var elist = elist || {};
elist.UI = elist.UI || {};

(function ($) {
    (function() {
        this.initListView = function(){
            $('#add_item').on('click', addItem);
            $('body').on('#add_item', 'click', addItem);
            $newItem = $('#new_item');

            runOnEnter($newItem, addItem);

            $newItem.focus();
        };

        function runOnEnter($target, action){
            $target.on('keyup', function(e){
                if (e.keyCode == 13) action();
            });
        }
    }).apply(elist.UI);
})(jQuery);
