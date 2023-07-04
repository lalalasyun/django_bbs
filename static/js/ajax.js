function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function sendPostForm(url,data,callback) {
    const method  = "POST";
    let form = data;

    if (! (data instanceof FormData)) {
        form = new FormData();
        for (const [key, value] of Object.entries(data)) {
            form.set(key,value);
        }
    } 
    $.ajax({
        url: url,
        type: method,
        data: form,
        processData: false,
        contentType: false,
        dataType: 'json'
    }).done( function(data, status, xhr ) { 
        if (data.redirect) {
            window.location.href = data.redirect;
        }
        if (data.content.messages) {
            $("#messages").html(data.content.messages);
        }
        callback(data, status, xhr);
    }).fail( function(xhr, status, error) {
        console.error(status + ":" + error );
    });
}