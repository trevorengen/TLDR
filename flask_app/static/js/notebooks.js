// jQuery methods
$(document).ready(function() {

    $('.notebooks-li').mouseenter(function(){
        $(this).animate({left: '20px'});
        $(this).css('font-style', 'italic');
    });

    $('.notebooks-li').mouseout(function(){
        $(this).animate({left: '0'});
        $(this).css('font-style', 'normal');
    });

    $('.notebooks-li').click(function(){
        var nb = $(this).attr('id');
        var targetUl = $('#bullet-ul');
        var targetTa = $('#queryta');
        $.post('/notebooks/retrieve', { notebook : nb })
            .done(function(data) {
                targetUl.empty();
                for (var i = 0; i < data.length; i++) {
                    var newLi = $('<li>');
                    newLi.appendTo(targetUl);
                    newLi.text(data[i]);
                }
                targetTa.prop('disabled', false);
                targetTa.attr('placeholder', 'Ask your notebook a question!');
            });
    });

    $('#ask').click(function(){
        var myTa = $('#queryta').val();
        $.post('/notebooks/query', { query : myTa })
            .done(function(data) {
                console.log(data);
            });
    });

    $('#add-bullet').click(function(){
        var targetUl = $('#bullet-ul');
        var newLi = $('<li>');
        var newText = $('<input>');
        newText.attr('type', 'text');
        newText.css({
            'width': '80%', 'border': '2px solid black', 
            'border-radius': '4px', 'height': '30px', 'outline': 'none',
            'padding-left': '3px',
        });
        newText.attr('id', 'temp-text');
        newLi.attr('id', 'temp');
        newText.appendTo(newLi);
        targetUl.prepend(newLi);
        newText.focus();
        newText.on('keypress', function(e) {
            if(e.which == 13){
                var text = $('#temp-text').val();
                $('#temp').remove();
                var newLi = $('<li>');
                newLi.text(text);
                $('#bullet-ul').prepend(newLi);
                $.post('/notebooks/addbullet', { bullet : text });
            }
        });
    });

    $('#delete-all').click(function(){
        if (!confirm('Are you sure?\n\nThis action cannot be undone.')) {
            return;
        } else {
            $.post('/notebooks/deletebullets')
                .done(function(result) {
                    if (result == 'Complete') {
                        $('#bullet-ul').empty();
                    }
                });
        }
    });
});