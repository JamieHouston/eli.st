var elist = elist || {};
elist.UI = elist.UI || {};

(function ($) {
    (function() {
        this.initListView = function(){

            loadItems();
            loadAttributes();

            $('body')
                .on('click', '#add_item', addItem)
                .on('click', '#show_item_details', toggleItemDetails)
                .on('click', '#add_attribute', addAttribute);

            $newItem = $('#new_item');

            runOnEnter($newItem, addItem);

            $newItem.focus();
        };

        this.initMarvin = function(){
            $('#command_form').submit(function(){
                runCommand();
                return false;
            });

            $('#command_text').focus();
        };

        function showCommandResults(result){
            showCommandResult(result);
            /*
            $div = $('<div>');
            for (key in result){
                $info = $('<div>');
                $info.text(key + ': ' + result[key]);
                $div.append($info);
            }
            $options = $('<div>');
            $options.append($('<span>').text('cancel'));
            $div.append($options);
            $('#command_result').html($div);
            $('#command_alert').show();
            $('#command_alert').alert();
            */
        }

        function toggleItemDetails(){
            var $details = $('.more-details');
            if ($details.first().is(':visible')){
                this.innerHTML = 'show details';
            } else {
                this.innerHTML = 'hide details';
            }
            $details.slideToggle();
        }

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

        function loadAttributes(){
            $.ajax('/attribute/all/', {
                success: function(data){
                    items = JSON.parse(data);
                    for (var i = items.length - 1; i >= 0; i--) {
                        addAttributeToList({pk: items[i].pk, name: items[i].fields.name});
                    }
                }
            });

        }

        function showCommandResult(command_result){
            template = getCommandTemplate(command_result);
            $('#items').prepend(template);
        }

        function addItemToList(item){
            template = getItemTemplate(item);
            $('#items').prepend(template);
        }

        function addAttributeToList(item){
            var option = $('<option value="' + item.name + '">' + item.name + '</option>');
            $('#item_attribute').append(option);
        }

        function runOnEnter($target, action){
            $target.on('keyup', function(e){
                if (e.keyCode == 13) {
                    e.preventDefault();
                    action();
                }
            });
        }

        function runCommand(){
            $.post('/command/',
                $('#command_form').serialize(),
                function(data){
                    result = data;
                    showCommandResults(result);
                    $('#command_text').val('').focus();
                }
            );
        }

        function addItem(){
            $.post('add/',
                $('#new_item_form').serialize(),
                function(data){
                    item = JSON.parse(data);
                    addItemToList(item);
                    $('#new_item').val('');
                }
            );
        }

        function addAttribute(){
            $.post('/attribute/add/',
                $('#new_attribute_form').serialize(),
                function(data){
                    item = JSON.parse(data);
                    addAttributeToList(item);
                    $('#new_attribute').val('');
                }
            );
        }

        function getCommandTemplate(command_result){
            var template = Handlebars.compile($('#command_info').html()),
            rendered = template(command_result);
            return rendered;
        }

        function getItemTemplate(item){
            var template = Handlebars.compile($('#item_row').html()),
            rendered = template(item);
            return rendered;
        }

    }).apply(elist.UI);
})(jQuery);
