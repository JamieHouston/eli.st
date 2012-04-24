var elist = elist || {};
elist.UI = elist.UI || {};

(function ($) {
    (function() {
        this.initListView = function(items){

            $('body').on('click', '#add_item', addItem);
            $newItem = $('#new_item');

            runOnEnter($newItem, addItem);

            for (var i = items.length - 1; i >= 0; i--) {
                this.addToList(items[i]);
            };

            $newItem.focus();
        };

        this.addToList = function(item){
            template = getItemTemplate(item);
            $('#items').prepend(template);

        }

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
                    this.addToList(item);
                    $('#new_item').val('');
                }
            });
        }

        function getItemTemplate(item){
            var template = Handlebars.compile($('#item_row').html()),
            rendered = template(item);
            return rendered;
        }

    }).apply(elist.UI);
})(jQuery);
