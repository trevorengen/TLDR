// jQuery methods
$(document).ready(function() {

    $('#side-container').hide();
    $('#arr-left').hide();
    $('.loader').hide();

    $('.notebooks-li').mouseover(function(){
        $(this).css('font-style', 'italic');
    });

    $('.notebooks-li').mouseout(function(){
        $(this).css('font-style', 'normal');
    });

    $('.delete-nb').click(function() {
        var notebookName = $(this).closest('div').attr('id');
        if (!confirm('Are you sure you want to delete ' + notebookName + '?\n\nThis action cannot be undone.')) {
            return;
        }
        $(this).closest('div').remove();
        $.post('/notebooks/delete', { nbName : notebookName })
    });

    $('.edit-nb').click(function() {
        // Conditional to prevent user from making a bunch of 
        // text boxes.
        if ($('#temp-text').attr('type') == 'text'){
            return;
        }
        var divItem = $(this).closest('div');
        var notebookName = divItem.attr('id');
        var listItem = $(this).siblings('li');
        listItem.css({'display': 'none'});
        var newText = $('<input>');
        newText.val(notebookName);
        newText.attr('type', 'text');
        newText.css({
            'width': '80%', 'border': '2px solid black', 
            'border-radius': '4px', 'height': '30px', 'outline': 'none',
            'padding-left': '3px', 'margin': '10px 30px',
        });
        newText.attr('id', 'temp-text');
        divItem.prepend(newText);
        newText.on('keypress', function(e) {
            if(e.which == 13){
                var text = $('#temp-text').val();
                var oldName = $('#temp-text').closest('div').attr('id');
                $.post('/notebooks/update', { new_name : text , old_name : oldName })
                    .done(location.reload());
            }
        });
    })

    $('#arr-left').click(function(){
        container = $('.notebook-side');
        container.animate({width: '60px'});
        side.hide();
        $('#arr-left').hide();
        $('#arr-right').delay(200).fadeIn(500);
    });

    $('#arr-right').click(function(){
        container = $('.notebook-side');
        side = $('#side-container');
        container.animate({width: '500px'});
        $('#arr-left').fadeIn(1300);
        $('#arr-right').hide();
        side.fadeIn(1000);
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
        if (myTa.length == 0) {
            return;
        }
        $('#ask').hide();
        $('.loader').show();
        var chkbox = $('#use-url').is(':checked');
        $.post('/notebooks/query', { query : myTa , checkbox : chkbox})
            .done(function(data) {
                $('#ask').show();
                $('.loader').hide();
                console.log(data);
                var question = $('<p>');
                var answer = $('<p>');
                var percent = $('<p>');
                var container = $('<div>');
                container.css({'margin': '20px 0'})
                question.text('Question: ' + $('#queryta').val());
                answer.text('Answer: ' + data['answer']);
                percent.text('Certainty: ' + String(Math.floor(100 * parseFloat(data['score'])) + '%'));
                container.append(question);
                container.append(answer);
                container.append(percent);
                $('#main-cont').append(container);
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

    $('#add-context').click(function(){
        var targetDiv = $('#url-add');
        var newText = $('<input>');
        newText.attr('type', 'text');
        newText.css({
            'width': '80%', 'border': '2px solid black', 
            'border-radius': '4px', 'height': '30px', 'outline': 'none',
            'padding-left': '3px', 'margin-top': '25px;',
        });
        newText.attr('id', 'temp-text');
        targetDiv.append(newText);
        newText.focus();
        newText.on('keypress', function(e) {
            if(e.which == 13){
                var text = $('#temp-text').val();
                $('#temp-text').remove()
                $.post('/addcontext', {url : text})
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