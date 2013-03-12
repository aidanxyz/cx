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
        },
        utils: {
            ajax_error_handler: function(jqXHR) {
                if (jqXHR.status == 401) {
                    alert("you need to login");
                }
                else {
                    alert($.parseJSON(jqXHR.responseText).message);
                }
            }
        }
    },
    mainpage: {
        onload: function(){
            return;
        }
    },
    review: {
        onload: function() {
            // adding feedback
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
                    form.siblings('ul').append(feedback);
                    // epmty the box
                    form.children('[name="feedback_body"]').val("");
                    // fire update function
                }).fail(function(jqXHR, textStatus, errorThrown) {
                    console.log(jqXHR);
                    var error = "";
                    $.each($.parseJSON(jqXHR.responseText), function(key, value) {
                        error += value + " ";
                    });
                    alert(error);
                });
                return false;
            });
            // voting
            $('.vote').on('click', function(){
                var link = $(this);
                var data_to_send = {'vote_type': link.attr('type-id')}
                var prev_link = link.siblings('.unvote');
                // is it re-vote?
                if (prev_link.length == 1) {
                    data_to_send.revote = true;
                }
                $.ajax({
                    data: data_to_send,
                    type: 'post',
                    url: '/feedbacks/' + link.parents('li').attr('feedback-id') + '/vote/',
                    dataType: 'json'
                }).done(function(data, textStatus, jqXHR) {
                    // change link attributes - '.unvote'
                    link.attr('class', 'unvote');
                    // feedback score
                    var score = link.parent().prev('span');
                    // count of votes of clicked link
                    var count = link.children('span#count');
                    // increment vote counter
                    count.text(parseInt(count.text()) + 1);
                    // add weight to feedback score
                    score.text(parseInt(score.text()) + parseInt(link.attr('weight')));
                    // if this was a re-vote
                    if (prev_link.length == 1) {
                        // subtract weight
                        var prev_count = prev_link.children('span#count');
                        prev_count.text(parseInt(prev_count.text()) - 1);
                        // subtract count
                        score.text(parseInt(score.text()) - parseInt(prev_link.attr('weight')));
                        // unset class .unvote
                        prev_link.attr('class', 'vote')
                    }
                    // fire update function
                }).fail(function(jqXHR, textStatus, errorThrown) {
                    siteNameSpace.common.utils.ajax_error_handler(jqXHR);
                }); 
            });
            // unvoting
            $('.unvote').on('click', function() {
                var link = $(this);
                $.ajax({
                    data: {'vote_type': link.attr('type-id')},
                    type: 'post',
                    url: '/feedbacks/' + link.parents('li').attr('feedback-id') + '/unvote/',
                    dataType: 'json'
                }).done(function(data, textStatus, jqXHR) {
                    // change link attributes - '.vote'
                    link.attr('class', 'vote');
                    // subtract from score
                    var score = link.parent().prev('span');
                    score.text(parseInt(score.text()) - parseInt(link.attr("weight")));
                    // decrement votes nuxmber
                    var count = link.children('span#count');
                    count.text(parseInt(count.text()) - 1);
                    // fire update function
                }).fail(function(jqXHR, textStatus, errorThrown) {
                    siteNameSpace.common.utils.ajax_error_handler(jqXHR);
                }); 
            });
            // marking as "I used this"
            $('a#used').click(function() {
                link = $(this);
                $.ajax({
                    type: 'post',
                    url: '/items/' + link.attr('item-id') + '/used/',
                    dataType: 'json'
                }).done(function(data, textStatus, jqXHR) {
                    link.parent('small').text("I used this");
                }).fail(function(jqXHR, textStatus, errorThrown) {
                    siteNameSpace.common.utils.ajax_error_handler(jqXHR);
                });
            })
        }
    },
    item_add: {
        onload: function() {
            fullTextSearch.init();
        }
    },
    detail_add: {
        onload: function() {
            $('form#detail').submit(function() {
                var form = $(this);
                var feedback_id = form.siblings('h1').attr('feedback-id');
                $.ajax({
                    url: '/feedbacks/' + feedback_id + '/details/add/',
                    data: form.serialize(),
                    type: 'post',
                    dataType: 'json'
                }).done(function(data, textStatus, jqXHR) {
                    var detail = ich.detail(data);
                    form.next('div#details').prepend(detail);
                    form.children('[name="body"]').val("");
                }).fail(function(jqXHR, textStatus, errorThrown) {
                    alert(jqXHR.responseText);
                });
                return false;
            });
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