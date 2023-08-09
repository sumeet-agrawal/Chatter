$(function() {
    $('#test').bind('click', function() {
        $.getJSON('/run', function(data){
        });
    })
});