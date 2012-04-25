var elist = elist || {};
elist.UI = elist.UI || {};

(function ($) {
    (function() {
        this.initListView = function(){

            loadItems();

            $('body').on('click', '#add_item', addItem);
            $newItem = $('#new_item');

            runOnEnter($newItem, addItem);

            $newItem.focus();
        };

        function loadItems(){
            $.ajax('/item/all/', {
                success: function(data){
                    items = JSON.parse(data);
                    for (var i = items.length - 1; i >= 0; i--) {
                        addItemToList({pk: items[i].pk, name: items[i].fields.name});
                    }
                }
            });
        }

        function addItemToList(item){
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
                    addItemToList(item);
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
