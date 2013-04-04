/* function is immediately executed; returns object closure */
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

/* returns object closure*/
function VoteHandler($this) {  //"$this" is a clicked link
    var prev_vote = $this.siblings('.unvote');
    var is_revote = prev_vote.length == 1;
    
    var feedback = $this.parents('li');

    function vote() {
        var data_to_send = {'vote_type': $this.attr('type-id')}
        if (is_revote) {
            data_to_send.is_revote = true;
        }
        
        var request = $.ajax({
            data: data_to_send,
            type: 'post',
            url: '/feedbacks/' + feedback.attr('id') + '/vote/',
            dataType: 'json'
        });

        request.done(function(data, textStatus, jqXHR) {
            affect_score(parseInt($this.attr('weight')));
            affect_count(1);
            change_class_to('unvote');
            // priority
            if (parseInt($this.attr('weight')) > 0) {
                add_set_priority();
            }
            else {
                remove_set_priority();
            }
        });

        request.fail(function(jqXHR, textStatus, errorThrown) {
            alert(jqXHR.responseText);
        });
    }

    function unvote() {
        var request = $.ajax({
            data: {'vote_type': $this.attr('type-id')},
            type: 'post',
            url: '/feedbacks/' + feedback.attr('id') + '/unvote/',
            dataType: 'json'
        });
        
        request.done(function(data, textStatus, jqXHR) {
            affect_score(-parseInt($this.attr('weight')));
            affect_count(-1);
            change_class_to('vote');
            // priority
            if (parseInt($this.attr('weight')) > 0) {
                remove_set_priority();
            }
        });

        request.fail(function(jqXHR, textStatus, errorThrown) {
            alert(jqXHR.responseText);
        });
    }

    function affect_score(weight) {
        var score = feedback.children('span#score');
        score.text(parseInt(score.text()) + weight);
        if (is_revote) {
            score.text(parseInt(score.text()) - parseInt(prev_vote.attr('weight')));
        }
    }

    function affect_count(weight) {
        var count = $this.children('span#count');
        inc_text_value(count, weight);
        //count.text(parseInt(count.text()) + weight);
        if (is_revote) {
            var prev_count = prev_vote.children('span#count');
            inc_text_value(prev_count, -weight);
            //prev_count.text(parseInt(prev_count.text()) - weight);
        }
    }

    function change_class_to(new_class) {
        $this.attr('class', opposite(opposite(new_class)));
        if (is_revote) {
            prev_vote.attr('class', opposite(new_class));
        }
    }

    function opposite(state) {
        if (state == 'vote') 
            return 'unvote';
        else
            return 'vote';
    }

    function add_set_priority() {
        var potential_priority = feedback.parents('div.span4').find('.unset_priority').length + 1 || 1; // patch hack
        if (potential_priority < 4) {
            feedback.children('#actions').append(ich.set_priority({value: potential_priority}))
        }
    }

    function remove_set_priority () {
        $this.siblings('.set_priority').text('');
    }

    return {
        vote: vote,
        unvote: unvote
    }
}

/* usual function; returns void */
function get_similars(query, url, results_wrapper, ich_id, add_data) {
    var results_list = results_wrapper.children('ul:first');
    var to_send = $.extend({'query': query}, add_data);
    var request = $.ajax({
        type: 'GET',
        url: url,
        data: to_send,
        dataType:'json',
    });

    request.done(function(data, textStatus, jqXHR) {
        if (data.length == 0) {
            results_wrapper.hide();
        }
        else {
            // clear the list
            results_list.html("");

            $.each(data, function(i, obj){
                // html_item = ich.similar_item({id: 5, name: 'some name'});
                html_elem = ich[ich_id](obj);
                results_list.append(html_elem);
            });
            results_wrapper.show();
        }
    });

    request.fail(function(jqXHR, textStatus, errorThrown) {
        alert(jqXHR.responseText);
    });
}

function PriorityHandler (wrapper_sel) {
    var max_set_priority = 0;
    // find latest set priority value
    $(wrapper_sel).find('.unset_priority').each(function(i) {
        var priority_val = parseInt($(this).text());
        if (priority_val > max_set_priority) {
            max_set_priority = priority_val;
        }
    });
    // console.log(wrapper_sel + ':' + max_set_priority);
    // set values to set_priorities without values (rendered by server)
    function affect_set_priority () {
        if (parseInt(max_set_priority) < 3) {
            // console.log('max_set_priority + 1: ' + parseInt(max_set_priority + 1));
            // console.log('number of .set_priority: ' + $(wrapper_sel).find('.set_priority').length);
            $(wrapper_sel).find('.set_priority').text(parseInt(max_set_priority) + 1);
        }
        else {
            $(wrapper_sel).find('.set_priority').text('');
        }
    }
    affect_set_priority();
    // setting priority
    $(wrapper_sel).on('click', '.set_priority', function () {
        var clickable = $(this);

        var feedback = clickable.parents('li');
        
        var request = $.ajax({
            url: '/feedbacks/' + feedback.attr('id') + '/priority/set/',
            data: {value: clickable.text()},
            type: 'post',
            dataType: 'json'
        });

        request.done(function(data, textStatus, jqXHR) {
            // change class to unset_priority
            clickable.attr('class', 'unset_priority');
            max_set_priority = parseInt(clickable.text());
            // increase values of .set_priority or remove them if priority-3 was clicked
            affect_set_priority();
            // increase priority stats counter
            var stat_counter = feedback.children('#info').find('span.priority#' + clickable.text());
            inc_text_value(stat_counter, 1);
        })

        request.fail(function(jqXHR, textStatus, errorThrown) {
            console.log(jqXHR);
            var error = "";
            $.each($.parseJSON(jqXHR.responseText), function(key, value) {
                error += value + " ";
            });
            alert(error);
        });
    });
    // unsetting priority
    $(wrapper_sel).on('click', '.unset_priority', function() {
        var clickable = $(this);
        var feedback = clickable.parents('li');

        // is this latest set priority
        if (parseInt(max_set_priority) !== parseInt(clickable.text())) {
            alert('Unset priority #' + max_set_priority + ' first');
            return false;
        }
        // request
        var request = $.ajax({
            url: '/feedbacks/' + feedback.attr('id') + '/priority/unset/',
            data: {value: clickable.text()},
            type: 'post',
            dataType: 'json'
        });

        request.done(function(data, textStatus, jqXHR) {
            // change class to set_priority
            clickable.attr('class', 'set_priority');
            // decrease potential priorities
            max_set_priority = parseInt(clickable.text()) - 1;
            affect_set_priority();
            // decrease priority stats counter
            var stat_counter = feedback.children('#info').find('span.priority#' + clickable.text());
            inc_text_value(stat_counter, -1);
        })

        request.fail(function(jqXHR, textStatus, errorThrown) {
            console.log(jqXHR);
            var error = "";
            $.each($.parseJSON(jqXHR.responseText), function(key, value) {
                error += value + " ";
            });
            alert(error);
        });
    });
    
    return {max_set_priority: max_set_priority}
}

function inc_text_value (dom_obj, n) {
    dom_obj.text(parseInt(dom_obj.text()) + n);
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
                // styling
                $('div#pros, div#cons').on({
                    mouseenter: function() {
                        $(this).find('.set_priority').show();
                    },
                    mouseleave: function() {
                        $(this).find('.set_priority').hide();
                    }
                }, 'li.well');
                // handling priorities
                var pros_priorities = PriorityHandler('div#pros');
                var cons_priorities = PriorityHandler('div#cons');
                // searching for positive/negative similar feedbacks 
                // grabs data from HTML div data-simi
                $('div[data-similars]').each(function(index) {
                    var options = $(this).data('similars');
                    var input = $(this).siblings('input[name=' + options.input_name + ']');
                    var results_wrapper = $(this);
                    var thread = null;
                    $(input).keyup(function() {
                        clearTimeout(thread);
                        thread = setTimeout(function(){
                            get_similars(input.val(), options.url, results_wrapper, options.ich_id, options.data);
                        }, 1000);
                    });
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
                        url: '/feedbacks/' + feedback.attr('id') + '/favorite/',
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
                    setTimeout(function() {
                        $('#not_used-modal').modal('hide');
                    }, 2500);
                });

                $('form#usage_form').submit(function() {
                    var form = $(this);
                    var forms = $('form#usage_form');

                    var request = $.ajax({
                        type: form.attr('method'),
                        url: form.attr('action'),
                        data: form.serialize(),
                        dataType: 'json'
                    });

                    request.done(function(data, textStatus, jqXHR) {
                        forms.after(ich.usage_info({
                            duration: form.find('select#id_duration option:selected').text(),
                            rating: form.find('select#id_rating option:selected').text()
                        }));
                        forms.remove();
                        // close modal if it was modal form
                        $('#not_used-modal').modal('hide');
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
            // fetching similar items
            var MIN_MODEL_NAME = 1;
            var similars_wrapper = $('div[data-similars]');
            var options = similars_$(wrapper_sel).data('similars');
            var input = similars_$(wrapper_sel).siblings('input[name=' + options.input_name + ']');
            var thread = null;
            $(input).keyup(function(){
                clearTimeout(thread);
                thread = setTimeout(function(){
                    get_similars(input.val(), options.url, similars_wrapper, options.ich_id);
                }, 1000);
            });
        }
    },
    details: {
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