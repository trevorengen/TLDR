// jQuery methods
$(document).ready(function() {

    $('.notebooks-li').mouseenter(function(){
        $(this).animate({left: '50px'});
        $(this).css('font-style', 'italic');
    });

    $('.notebooks-li').mouseout(function(){
        $(this).animate({left: '0'});
        $(this).css('font-style', 'normal');
    });

    $('.notebooks-li').click(function(){
        var nb = $(this).attr('id');
        var targetUl = $('#bullet-ul');
        $.post('/notebooks/retrieve', { notebook : nb })
            .done(function(data) {
                targetUl.empty();
                for (var i = 0; i < data.length; i++) {
                    var newLi = $('<li>');
                    newLi.appendTo(targetUl);
                    newLi.text(data[i]);
                }
            });
    });
    
});