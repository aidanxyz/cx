var djangoAjaxCsrf = {
    init: function(cookie_name){
        $.ajaxSetup({
            crossDomain: false, // obviates need for sameOrigin test
            beforeSend: function(xhr, settings) {
                if (!this.isSafeMethod(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", this.getCookieValue(cookie_name));
                }
            }
        });
    },
    getCookieValue: function(name){
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },
    isSafeMethod: function (method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
}

djangoAjaxCsrf.init('csrftoken');