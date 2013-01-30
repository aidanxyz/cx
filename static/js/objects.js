// module pattern
var djangoAjaxCsrf = (function(){
    var config  = {
        cookie_name: 'csrftoken',
        cookie_val: null
    }

    function init() {
        $.ajaxSetup({
            crossDomain: false, // obviates need for sameOrigin test
            beforeSend: function(xhr, settings) {
                if (!isSafeMethod(settings.type)) {
                    if (config.cookie_val == null) {
                        config.cookie_val = getCookieValue(config.cookie_name);
                    }
                    xhr.setRequestHeader("X-CSRFToken", config.cookie_val);
                }
            }
        });
    }

    function getCookieValue(name) {
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
    }

    function isSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    return {
        init: init
    }
})();

// module pattern
var fullTextSearch = (function() {
	var config = {
		formSelector: "#id_name",
        url: '/items/search',
        timeout: 1000
	}

	function handleResults(data, textStatus, jqXHR) {
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
	}

	function init() {
		var thread = null;
        $(config.formSelector).keyup(function(){
        	clearTimeout(thread);
        	var form = $(this);
            thread = setTimeout(function(){
            	search(form.val());
            }, config.timeout);
        });
	}

	function search(query) {
		$.ajax({
            type: 'GET',
            url: config.url,
            data: {'query': query},
            dataType:'json',
            success: handleResults
        });
	}

	return {
		config: config, 
		init: init,
		handleResults: handleResults
	}
})();



// object literal pattern
var siteNameSpace = {
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
            $('form#feedback').submit(function(){
                var form = $(this);
                if (form.children('[name="feedback_body"]').val() == '') {
                    return false;
                }
                $.ajax({
                    data: $(this).serialize(),
                    type: $(this).attr('method'),
                    url:  $(this).attr('action'),
                    dataType: 'json'
                }).done(function(data, textStatus, jqXHR) {
                    var feedback = ich.feedback(data);
                    form.before(feedback);
                    // epmty the box
                    form.children('[name="feedback_body"]').val("");
                }).fail(function(jqXHR, textStatus, errorThrown) {
                    console.log(jqXHR);
                    var error = "";
                    $.each($.parseJSON(jqXHR.responseText), function(key, value) {
                        error += value + " ";
                    });
                    alert(error);
                })
                return false;
            });
        }
    },
    item_add: {
        onload: function() {
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