var djangoAjaxCsrf = {
    config: {
        cookie_name: 'csrftoken'
    },
    init: function(){
        $.ajaxSetup({
            crossDomain: false, // obviates need for sameOrigin test
            beforeSend: function(xhr, settings) {
                if (!djangoAjaxCsrf.isSafeMethod(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", djangoAjaxCsrf.getCookieValue(djangoAjaxCsrf.cookie_name));
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

var fullTextSearch = {
    config: {
        formSelector: "#id_name",
        url: '/items/search',
        timeout: 1000
    },
    resultsHandler: function(data, textStatus, jqXHR){
        if (data.length == 0) {
            $('div#similar_items').hide();
        }
        else {
            // clear the list
            console.log(data);
            $('p#similar_item').remove();
            $.each(data, function(i, item_obj){
                item = ich.similar_item({
                    id: item_obj.pk, 
                    name: item_obj.fields.name
                });
                console.log(item);
                // append template to '#similar_items' div-box
                $('div#similar_items').append(item);
            });
            // display 'similar_items' div-box
            $('div#similar_items').show();
        }
    },
    init: function(){
        var thread = null;
        $(fullTextSearch.config.formSelector).keyup(function(){
            clearTimeout(thread);
            var form = $(this);
            thread = setTimeout(function(){
                fullTextSearch.search(form.val());
            }, fullTextSearch.config.timeout);
        });
    },
    search: function(query){
        $.ajax({
            type: 'GET',
            url: fullTextSearch.config.url,
            data: {'query': query},
            dataType:'json',
            success: fullTextSearch.resultsHandler
        });
    }
}

// object literal pattern
var cxNameSpace = {
    common : {
        onload: function() {
            djangoAjaxCsrf.init();
        }
    },
    mainpage: {
        onload: function(){
            return;
        }
    },
    review: {
        onload: function() {
            return;
        }
    },
    item_add: {
        onload: function() {
            fullTextSearch.resultsHandler = function(data, textStatus, jqXHR) {
                // custom stuff
            }
            fullTextSearch.init();
        }
    },
    login: {
        onload: function() {
            return;
        }
    },
    apply: function(page) {
        this.common.onload();
        this[page].onload();
    }
}