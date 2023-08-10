$(function() {
    $('#sendBtn').bind('click', function() {
        let value = document.getElementById("msg").value
        $.getJSON('/send_message', 
            {val: value}, 
            function(data){
        });
    })
});

window.addEventListener("load", function(){
    var update_timer = this.setInterval(update, 100);
});

function update() {
    fetch('/get_messages')
        .then(function(response) {
                return response.text()
        }).then(function(text) {
            console.log(text.length)
            if(text.length > 3)
                document.getElementById("prevMsg").innerHTML += text + "<br >"
        })    
}