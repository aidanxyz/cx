// module pattern
var DjangoAjaxCsrf = (function(){
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

function VoteHandler($this) {  //"$this" is a clicked link
    var prev_vote = $this.siblings('.unvote');
    var revote = prev_vote.length == 1;
    
    var feedback = $this.parents('li');

    function vote() {
        var data_to_send = {'vote_type': $this.attr('type-id')}
        if (revote) {
            data_to_send.revote = true;
        }
        
        var request = $.ajax({
            data: data_to_send,
            type: 'post',
            url: '/feedbacks/' + feedback.attr('feedback-id') + '/vote/',
            dataType: 'json'
        });

        request.done(function(data, textStatus, jqXHR) {
            affect_score(parseInt($this.attr('weight')));
            affect_count(1);
            // change class of clicked link
            change_class_to('unvote');
        });

        request.fail(function(jqXHR, textStatus, errorThrown) {
            alert(jqXHR.responseText);
        });
    }

    function unvote() {
        var request = $.ajax({
            data: {'vote_type': $this.attr('type-id')},
            type: 'post',
            url: '/feedbacks/' + feedback.attr('feedback-id') + '/unvote/',
            dataType: 'json'
        });
        
        request.done(function(data, textStatus, jqXHR) {
            affect_score(-parseInt($this.attr('weight')));
            affect_count(-1);
            change_class_to('vote');
        });

        request.fail(function(jqXHR, textStatus, errorThrown) {
            alert(jqXHR.responseText);
        });
    }

    function affect_score(weight) {
        var score = feedback.children('span#score');
        score.text(parseInt(score.text()) + weight);
        if (revote) {
            score.text(parseInt(score.text()) - parseInt(prev_vote.attr('weight')));
        }
    }

    function affect_count(weight) {
        var count = $this.children('span#count');
        count.text(parseInt(count.text()) + weight);
        if (revote) {
            var prev_count = prev_vote.children('span#count');
            prev_count.text(parseInt(prev_count.text()) - weight);
        }
    }

    function change_class_to(new_class) {
        $this.attr('class', opposite(opposite(new_class)));
        if (revote) {
            prev_vote.attr('class', opposite(new_class));
        }
    }

    function opposite(state) {
        if (state == 'vote') 
            return 'unvote';
        else
            return 'vote';
    }

    return {
        vote: vote,
        unvote: unvote
    }
}

function SearchWhileTyping(config) {

    var input_sel   = config.input_sel, 
        url         = config.url, 
        timeout     = config.timeout,
        ich_id      = config.ich_id,    // id of ich template
        results_sel = config.results_sel,   // element containing search results
        wrapper_sel = config.wrapper_sel,   // parent of results element
        data        = typeof config.data === 'object' ? config.data : null;

    function init() {
        var thread = null;
        $(input_sel).keyup(function(){
            clearTimeout(thread);
            var form = $(this);
            thread = setTimeout(function(){
                search(form.val());
            }, timeout);
        });
    }

    function search(query) {
        var to_send = $.extend({'query': query}, data);

        var request = $.ajax({
            type: 'GET',
            url: url,
            data: to_send,
            dataType:'json',
        });

        request.done(function(data, textStatus, jqXHR) {
            if (data.length == 0) {
                $(wrapper_sel).hide();
            }
            else {
                // clear the list
                $(results_sel).html("");

                $.each(data, function(i, obj){
                    // html_item = ich.similar_item({id: 5, name: 'some name'});
                    html_elem = ich[ich_id](obj);
                    $(results_sel).append(html_elem);
                });
                $(wrapper_sel).show();
            }
        });

        request.fail(function(jqXHR, textStatus, errorThrown) {
            alert(jqXHR.responseText);
        });
    }

    init();
}

// object literal pattern
var siteNameSpace = {
    common : {
        config: {},
        init: function() {
            DjangoAjaxCsrf.init();
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
        },
    },
    mainpage: {
        init: function(){
            return;
        }
    },
    review: {
        config: {
            is_authenticated: false,
        },
        init: function(config) {
            if (config && typeof config === 'object') {
                $.extend(this.config, config);
            }
            if (this.config.is_authenticated) { // this = review object
                this.authenticated[this.config.is_used ? 'used' : 'not_used']();
            }
            else {
                this.guest();
            }
        },
        guest: function() {
            $('.vote, .unvote, a#add_feedback, a#used').click(function() {
                $('#login-modal').modal();
            });
        },
        authenticated: {
            used: function() {
                // searching for positive similar feedbacks
                SearchWhileTyping({
                    url: 'feedbacks/search/',
                    data: {
                        item_id: $('div#item_info').attr('item-id'), 
                        is_positive: 1
                    },
                    input_sel: '#feedback_body-1',
                    timeout: 1000,
                    ich_id: 'similar_feedback',
                    results_sel: 'ul#results_list-1',
                    wrapper_sel: 'div#similar_items-1'
                });
                // searching for negative similar feedbacks
                SearchWhileTyping({
                    url: 'feedbacks/search/',
                    data: {
                        item_id: $('div#item_info').attr('item-id'), 
                        is_positive: 1
                    },
                    input_sel: '#feedback_body-0',
                    timeout: 1000,
                    ich_id: 'similar_feedback',
                    results_sel: 'ul#results_list-0',
                    wrapper_sel: 'div#similar_items-0'
                });
                // adding feedback
                $('form#add_feedback').submit(function(){
                    var form = $(this);
                    if (form.children('[name="feedback_body"]').val() == '') {
                        return false;
                    }

                    var request = $.ajax({
                        data: $(this).serialize(),
                        type: $(this).attr('method'),
                        url:  $(this).attr('action'),
                        dataType: 'json'
                    });

                    request.done(function(data, textStatus, jqXHR) {
                        var feedback = ich.feedback(data);
                        form.siblings('ul').append(feedback);
                        form.children('[name="feedback_body"]').val("");
                        // fire update function
                    });

                    request.fail(function(jqXHR, textStatus, errorThrown) {
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
                $(document).on('click', '.vote', function(){
                    console.log('click on .vote');
                    VoteHandler($(this)).vote();
                });
                // unvoting
                $(document).on('click', '.unvote', function(){
                    console.log('click on .unvote');
                    VoteHandler($(this)).unvote();
                });
                // favoriting
                $(document).on('click', '.favorite', function() {
                    var link = $(this);
                    feedback = link.parents('li');
                    var request = $.ajax({
                        url: '/feedbacks/' + feedback.attr('feedback-id') + '/favorite/',
                        type: 'post',
                        dataType: 'json'
                    });

                    request.done(function(data, textStatus, jqXHR) {
                        $(this).attr('class', 'unfavorite');
                        // hide others since we can choose only one favorite 
                        $('.favorite').hide();
                    });
                })
            },
            not_used: function() {
                // <I used it> click
                $('button#used').click(function() {
                    $('a#used').trigger('click');
                    $(this).text('Saving...');
                    setTimeout(function() {
                        $('#not_used-modal').modal('hide');
                    }, 1000);
                });

                $('form#usage_form').submit(function() {
                    var form = $(this);
                    var request = $.ajax({
                        type: form.attr('method'),
                        url: form.attr('action'),
                        data: form.serialize(),
                        dataType: 'json'
                    });

                    request.done(function(data, textStatus, jqXHR) {
                        form.after(ich.usage_info({
                            duration: $('select#id_duration option:selected').text(),
                            rating: $('select#id_rating option:selected').text()
                        }));
                        form.remove();
                        // switch event handlers to allow voting etc.
                        $('.vote, .unvote, a#add_feedback').off('click');
                        siteNameSpace.review.authenticated.used();
                        // remove "Add feedback" links and show forms
                        $('a#add_feedback').remove();
                        $('form#add_feedback').show();
                    });

                    request.fail(function(jqXHR, textStatus, errorThrown) {
                        siteNameSpace.common.utils.ajax_error_handler(jqXHR);
                    });

                    return false;
                });
                // voting, unvoting, adding a feedback on unused state
                $('.vote, .unvote, a#add_feedback').click(function() {
                    $('#not_used-modal').modal();
                });
            }
        },
    },
    item_add: {
        init: function() {
            SearchWhileTyping({
                url: '/items/search',
                input_sel: '#id_name',
                timeout: 1000,
                ich_id: 'similar_item',
                results_sel: 'ul#results_list',
                wrapper_sel: 'div#similar_items'
            });
        }
    },
    detail_add: {
        init: function() {
            // adding detail
            $('form#detail').submit(function() {
                var form = $(this);
                var feedback_id = form.siblings('h1').attr('feedback-id');
                
                var request = $.ajax({
                    url: '/feedbacks/' + feedback_id + '/details/add/',
                    data: form.serialize(),
                    type: 'post',
                    dataType: 'json'
                });

                request.done(function(data, textStatus, jqXHR) {
                    var detail = ich.detail(data);
                    form.next('div#details').prepend(detail);
                    form.children('[name="body"]').val("");
                });

                request.fail(function(jqXHR, textStatus, errorThrown) {
                    alert(jqXHR.responseText);
                });
                return false;
            });
        }
    },
    login: {
        init: function() {
            return;
        }
    },
    exec: function(page, config) {
        this.common.init();
        this[page]['init'](config);
    }
}