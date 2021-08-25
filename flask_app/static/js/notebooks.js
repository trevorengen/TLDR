// jQuery methods
$(document).ready(function() {

    $('.notebooks-li').mouseover(function(){
        $(this).css('font-style', 'italic');
    });

    $('.notebooks-li').mouseout(function(){
        $(this).css('font-style', 'normal');
    });

    $('.delete-nb').click(function() {
        notebookName = $(this).closest('div').attr('id');
        if (!confirm('Are you sure you want to delete ' + notebookName + '?\n\nThis action cannot be undone.')) {
            return;
        }
        $(this).closest('div').remove();
        $.post('/notebooks/delete', { nbName : notebookName })
    });

    $('.notebooks-li').click(function(){
        var nb = $(this).text();
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

    $('#add-nb').click(function() {
        var targetUl = $('#notebook-ul');
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
                
                $.post('/notebooks/add', { name : text })
                    .done(location.reload());
            }
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

    $('#create-new').click(function() {
        $('#notebook-pop').css('display', 'block');
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