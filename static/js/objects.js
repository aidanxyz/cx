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
        var score = feedback.children('div#score');
        score.text(parseInt(score.text()) + weight);
        if (is_revote) {
            score.text(parseInt(score.text()) - parseInt(prev_vote.attr('weight')));
        }
    }

    function affect_count(weight) {
        var count = get_count_obj($this.attr('type-id'));
        count.text(parseInt(count.text()) + weight);
        if (is_revote) {
            var prev_count = get_count_obj(prev_vote.attr('type-id'));
            prev_count.text(parseInt(prev_count.text()) - weight);
        }
    }

    function get_count_obj (type_id) {
        if (type_id == '1') {
            return feedback.children('div#stats').children('span#agrees_count');
        }
        else if (type_id == '2') {
            return feedback.children('div#stats').children('span#disagrees_count');
        }
    }

    function change_class_to(new_class) {
        if (new_class == 'unvote') {
            $this.removeClass('vote');
            $this.addClass('unvote active');
            if (is_revote) {
                prev_vote.removeClass('unvote active');
                prev_vote.addClass('vote');
            }
        }
        else if (new_class == 'vote') {
            $this.removeClass('unvote active');
            $this.addClass('vote');
        }
    }

    function add_set_priority() {
        var potential_priority = feedback.parents('div.feedback_column').find('.unset_priority').length + 1 || 1; // patch hack
        if (potential_priority < 4) {
            feedback.children('#actions').append(ich.set_priority({value: potential_priority}))
        }
    }

    function remove_set_priority () {
        $this.siblings('.set_priority').remove();
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

    if (query.length < 2) {
        results_list.html("");
        results_wrapper.hide();
        return;
    }
    
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
        var priority_val = parseInt($(this).text().substring(1)); // ex.: '#2'.substring(1) = '2'
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
            $(wrapper_sel).find('.set_priority').text('#' + (max_set_priority + 1));//.show();
        }
        else {
            $(wrapper_sel).find('.set_priority').remove();//text('').hide();
        }
    }
    affect_set_priority();
    // setting priority
    $(wrapper_sel).on('click', '.set_priority', function () {
        var clickable = $(this);

        var feedback = clickable.parents('li');
        
        var request = $.ajax({
            url: '/feedbacks/' + feedback.attr('id') + '/priority/set/',
            data: {value: clickable.text().substring(1)},
            type: 'post',
            dataType: 'json'
        });

        request.done(function(data, textStatus, jqXHR) {
            // change class to unset_priority
            clickable.removeClass('set_priority');
            clickable.addClass('unset_priority active');
            max_set_priority = parseInt(clickable.text().substring(1)); // this comes before affecting sets
            // increase values of .set_priority or remove them if priority-3 was clicked
            affect_set_priority();
            // increase priority stats counter
            var stat_counter = feedback.children('div#stats').find('span.priority#' + clickable.text().substring(1));
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
        var clicked_priority_val = clickable.text().substring(1);

        // is this latest priority that was set by user
        if (parseInt(max_set_priority) !== parseInt(clicked_priority_val)) {
            alert('Unset priority #' + max_set_priority + ' first');
            return false;
        }
        // request
        var request = $.ajax({
            url: '/feedbacks/' + feedback.attr('id') + '/priority/unset/',
            data: {value: clicked_priority_val},
            type: 'post',
            dataType: 'json'
        });

        request.done(function(data, textStatus, jqXHR) {
            // change class to set_priority
            clickable.removeClass('unset_priority active');
            clickable.addClass('set_priority');
            // decrease potential priorities
            max_set_priority = parseInt(clicked_priority_val) - 1;
            affect_set_priority();
            // decrease priority stats counter
            var stat_counter = feedback.children('div#stats').find('span.priority#' + clicked_priority_val);
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

function other_reason_adapt (radio_id, input_id) {
    $('input:radio#' + radio_id).change(function() {
        $('input:text#' + input_id).removeAttr('disabled').focus();
    });
    $('input:radio').not('#' + radio_id).change(function() {
        $('input:text#' + input_id).attr('disabled', '');
    });
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
    base: {
        init: function(){
            $('input#search_input').typeahead({
                source: function(query, process) {
                    urls = {}
                    if (query.length > 4) {
                        $.get('/items/search/', {query: query}, function(data) {
                            var results = [];
                            data = $.parseJSON(data);
                            $.each(data, function(i, object) {
                                results[i] = object.name;
                                urls[object.name] = object.id;
                            });
                            process(results);
                        });
                    }
                },
                updater: function(item) {
                    setTimeout(function() {
                        window.location.href = '/items/' + urls[item] + '/';
                    }, 100);
                    return item;
                }
            });
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
            // Enabel specification tooltips
            $('div#specifications a').tooltip({placement: 'bottom'});
            // Toggle actions
            $('button#hide_actions').click(function() {
                $('div#actions').toggle();
                $('div#stats').toggle();
                if ($(this).hasClass('active')) {
                    $(this).removeClass('active');
                }
                else {
                    $(this).addClass('active');
                }
            });
        },
        guest: function() {
            $('.vote, .unvote, a#add_feedback, a#used, #usage_submit').click(function() {
                $('#login-modal').modal();
                return false;
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
                }, 'li.feedback');
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
                        // hide similars
                        $('div#similars').hide();
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

                    request.fail(function(jqXHR, textStatus, errorThrown) {
                        alert("Something went wrong");
                    });
                });
                // suggesting an edit
                $('div#proscons_wrapper').on('click', 'a#suggest_edit', function() {
                    var clickable = $(this);
                    var feedback = clickable.parents('li.feedback');
                    var feedback_body = feedback.children('div#feedback_body').text();
                    var suggest_edit_modal = $('div#suggest_edit-modal');

                    var suggest_edit_form = ich.suggest_edit_form({
                        feedback_id: feedback.attr('id'), 
                        feedback_body: feedback_body,
                    });
                    console.log(feedback_body);
                    suggest_edit_modal.find('div#dynamic_content').html(suggest_edit_form);
                    suggest_edit_modal.find('input[name=suggested_value]').focus();
                    suggest_edit_modal.modal('show');
                });
                // submitting suggest
                $('div#item').on('submit', 'form#suggest_edit', function() {
                    var form = $(this);
                    var request = $.ajax({
                       url: form.attr('action'),
                       type: form.attr('method'),
                       data: form.serialize(),
                    });

                    request.done(function(data, textStatus, jqXHR) {
                        var suggest_edit_modal = $('div#suggest_edit-modal');
                        suggest_edit_modal.find('div#dynamic_content').html("<div id='thanks'>Thanks!</div>");
                        setTimeout(function(){
                            suggest_edit_modal.modal('hide');
                        }, 1000);
                    });

                    request.fail(function(jqXHR, textStatus, errorThrown) {
                        alert("Something went wrong");
                    });
                    return false;
                });
            },
            not_used: function() {
                $('form#usage_form').submit(function() {
                    var form = $(this);

                    var request = $.ajax({
                        type: form.attr('method'),
                        url: form.attr('action'),
                        data: form.serialize(),
                        dataType: 'json'
                    });

                    request.done(function(data, textStatus, jqXHR) {
                        // switch event handlers to allow voting etc.
                        $('.vote, .unvote, a#add_feedback').off('click');
                        siteNameSpace.review.authenticated.used();
                        // remove "Add feedback" links and show forms
                        $('a#add_feedback').remove();
                        $('form#add_feedback').show();
                        // close modal
                        $('div#not_used-modal').modal('hide');
                        $('div#item_name').append('<i class="icon-ok-sign icon-white" id="icon_used"></i>');
                        $('span#item_rating').text(data['avg_rating'] + '/5');
                        $('div#reviewers_count span').text(data['reviewers_count']);
                        $('a#used').replaceWith(ich.user_rating(data));
                    });

                    request.fail(function(jqXHR, textStatus, errorThrown) {
                        siteNameSpace.common.utils.ajax_error_handler(jqXHR);
                    });

                    return false;
                });
                // voting, unvoting, adding a feedback on unused state
                $('.vote, .unvote, a#add_feedback, a#used').click(function() {
                    $('div#not_used-modal').modal('show');
                });
            }
        },
    },
    item_add: {
        init: function() {
            // fetching similar items
            var similars_wrapper = $('div[data-similars]');
            var options = similars_wrapper.data('similars');
            var input = similars_wrapper.siblings('input[name=' + options.input_name + ']');
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
                    data: {body: tinyMCE.activeEditor.getContent()},
                    type: 'post',
                    dataType: 'json'
                });

                request.done(function(data, textStatus, jqXHR) {
                    console.log($('<div/>').html(String(data.body)).contents());
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
    moderate: {
        init: function(config) {
            if (config.page == 'items') {
                this.items();
            }
            else if (config.page == 'feedback') {
                this.feedback();
            }
            else if (config.page == 'prices') {
                this.prices();
            }
            else if (config.page == 'images') {
                this.images();
            };
        },
        items: function() {
            $('button#approve').click(function() {
                var clickable = $(this);
                var item_div = clickable.parents('div.item');
                var request = $.ajax({
                    url: '/items/' + item_div.attr('id') + '/approve/',
                    type: 'post',
                    dataType: 'json',
                });

                request.done(function(data, textStatus, jqXHR) {
                    clickable.addClass('active btn-success');
                    clickable.html("<i class='icon-ok icon-white'></i> Approved");
                    setTimeout(function() {
                        item_div.fadeOut('slow');
                    }, 2000);
                });

                request.fail(function(jqXHR, textStatus, errorThrown) {
                    // var data = $.parseJSON(jqXHR.responseText);
                    if (data.status) {
                        var action = (data.status == 'AP') ? 'approved' : 'deactivated';
                        alert("Was already " + action + " by " + data.moderated_by);
                    }
                    else 
                        alert("Something went wrong.");
                });
            });

            $('a#duplicates').click(function() {
                var clickable = $(this);
                var request = $.ajax({
                    url: '/items/' + clickable.attr('item-id') + '/duplicates/',
                    type: 'post',
                    dataType: 'json',
                });
                
                request.done(function(data, textStatus, jqXHR) {
                    // data = $.parseJSON(jqXHR.responseText);
                    ul = clickable.siblings('div#similar_items').children('ul:first');
                    $.each(data, function(i) {
                        var similar_item = ich.similar_item({id: i, name: data[i]});
                        ul.append(similar_item);
                    });
                    ul.parent().show();
                    // disable this functionality
                    clickable.attr('id', 'duplicates_got');
                });

                request.fail(function(jqXHR, textStatus, errorThrown) {
                    alert("Something went wrong");
                });
            });

            $('div#duplicates').on('click', 'button#duplicate', function() {
                var clickable = $(this);
                var item_div = clickable.parents('div.item');
                var request = $.ajax({
                    url: '/items/' + item_div.attr('id') + '/deactivate/',
                    type: 'post',
                    dataType: 'json',
                    data: {reason: 1, duplicate_of: clickable.attr('duplicate_of')} // reason:1 means 'duplicate'
                });

                request.done(function(data, textStatus, jqXHR) {
                    item_div.css("background-color", "red");
                    setTimeout(function () {
                        item_div.fadeOut("slow");
                    }, 1000);
                });

                request.fail(function(jqXHR, textStatus, errorThrown) {
                    alert("Something went wrong");
                });
            });

            $('button#spam').click(function() {
                var clickable = $(this);
                var item_div = clickable.parents('div.item');
                var request = $.ajax({
                    url: '/items/' + item_div.attr('id') + '/deactivate/',
                    type: 'post',
                    dataType: 'json',
                    data: {reason: 2} // reason:2 means 'Non-relevant (spam)'
                });

                request.done(function(data, textStatus, jqXHR) {
                    item_div.css("background-color", "red");
                    setTimeout(function () {
                        item_div.fadeOut("slow");
                    }, 1000);
                });

                request.fail(function(jqXHR, textStatus, errorThrown) {
                    alert("Something went wrong");
                });
            });
        },
        feedback: function() {
            $('a#accept').click(function() {
                var clickable = $(this);
                var suggestion_id = clickable.parents('tr').attr('id');
                
                var request = $.ajax({
                    url: '/feedbacks/suggestions/' + suggestion_id + '/accept/',
                    type: 'post',
                    dataType: 'json'
                });

                request.done(function(data, textStatus, jqXHR) {
                    var row = clickable.parents('tr');
                    row.css("background-color", "green");
                    setTimeout(function(){
                        row.fadeOut("slow");
                    }, 1000);
                });

                request.fail(function(jqXHR, textStatus, errorThrown) {
                    alert("Something went wrong");
                });
            });

            $('a#ignore').click(function() {
                var clickable = $(this);
                var suggestion_id = clickable.parents('tr').attr('id');
                
                var request = $.ajax({
                    url: '/feedbacks/suggestions/' + suggestion_id + '/ignore/',
                    type: 'post',
                    dataType: 'json'
                });

                request.done(function(data, textStatus, jqXHR) {
                    var row = clickable.parents('tr');
                    row.css("background-color", "blue");
                    setTimeout(function(){
                        row.fadeOut("slow");
                    }, 1000);
                });

                request.fail(function(jqXHR, textStatus, errorThrown) {
                    alert("Something went wrong");
                });
            });
        },
        prices: function() {
            $('a#approve').click(function() {
                var clickable = $(this);
                var price_id = clickable.parents('tr').attr('id');
                
                var request = $.ajax({
                    url: '/items/prices/' + price_id + '/approve/',
                    type: 'post',
                    dataType: 'json'
                });

                request.done(function(data, textStatus, jqXHR) {
                    var row = clickable.parents('tr');
                    row.css("background-color", "green");
                    setTimeout(function(){
                        row.fadeOut("slow");
                    }, 1000);
                });

                request.fail(function(jqXHR, textStatus, errorThrown) {
                    alert("Something went wrong");
                });
            });

            $('a#ignore').click(function() {
                var clickable = $(this);
                var price_id = clickable.parents('tr').attr('id');
                
                var request = $.ajax({
                    url: '/items/prices/' + price_id + '/ignore/',
                    type: 'post',
                    dataType: 'json'
                });

                request.done(function(data, textStatus, jqXHR) {
                    var row = clickable.parents('tr');
                    row.css("background-color", "blue");
                    setTimeout(function(){
                        row.fadeOut("slow");
                    }, 1000);
                });

                request.fail(function(jqXHR, textStatus, errorThrown) {
                    alert("Something went wrong");
                });
            });
        },
        images: function() {
            $('button#make_cover').click(function() {
                var clickable = $(this);
                var request = $.ajax({
                    url: clickable.attr('url'),
                    data: {image_id: clickable.attr('image-id')},
                    type: 'post',
                    dataType: 'json'
                });

                request.done(function(data, textStatus, jqXHR) {
                    $('i.icon-star').remove();
                    clickable.parent('li').after("<i class='icon-star'></i>");
                });

                request.fail(function(jqXHR, textStatus, errorThrown) {
                    alert('Something went wrong');
                });
            });
        },
    },
    edit_item: {
        init: function () {
            $('input:text#id_other_reason').attr('disabled', '');
            other_reason_adapt('id_reason_1', 'id_other_reason');
            // fetching similar items
            var similars_wrapper = $('div[data-similars]');
            var options = similars_wrapper.data('similars');
            var input = $('input[name=' + options.input_name + ']');
            var thread = null;
            $(input).keyup(function(){
                clearTimeout(thread);
                thread = setTimeout(function(){
                    get_similars(input.val(), options.url, similars_wrapper, options.ich_id);
                }, 1000);
            });
        }
    },
    home: {
        init: function() {
            $('input[name=query]').typeahead({
                source: function(query, process) {
                    urls = {}
                    if (query.length > 4) {
                        $.get('/items/search/', {query: query}, function(data) {
                            var results = [];
                            data = $.parseJSON(data);
                            $.each(data, function(i, object) {
                                results[i] = object.name;
                                urls[object.name] = object.id;
                            });
                            process(results);
                        });
                    }
                },
                updater: function(item) {
                    setTimeout(function() {
                        window.location.href = '/items/' + urls[item] + '/';
                    }, 100);
                    return item;
                }
            });

            $.get('/items/latest/5/', {}, function(data) {
                data = $.parseJSON(data);
                var link = $('div#search_example a#item_name');
                link.text(data[0].name);
                link.attr('href', '/items/' + data[0] + '/');
                
                var i = 1;
                function showLatestItems() {
                    setTimeout(function() {
                        if (data.length > i) {
                            link.fadeOut("slow", function() {
                                link.text(data[i].name);
                                link.attr('href', '/items/' + data[i].id + '/');
                            });
                            link.fadeIn("fast");
                            i += 1;
                        }
                        else {
                            i = 0;
                        }
                        showLatestItems();
                    }, 3000);
                }

                showLatestItems();
            });
        }
    },
    stats: {
        init: function(options) {
            if (options.page == 'item') {
                this.item();
            }
            else if (options.page == 'feedback') {
                this.feedback();
            }
        },
        item: function() {
            // Load the Visualization API and the piechart package.
            google.load('visualization', '1', {'packages':['corechart'], 'callback': drawChart});

            // Set a callback to run when the Google Visualization API is loaded.
            // google.setOnLoadCallback(drawChart);

            function drawChart() {
                var item_id = $('div.item').attr('id');
                var jsonData = $.ajax({
                    url: '/items/' + item_id + '/get_stats/',
                    type: "get",
                    dataType:"json",
                    async: false,
                }).responseText;

                jsonData = $.parseJSON(jsonData);
                console.log(jsonData);

                $.each(jsonData, function(i, object) {
                    if (i != 'prices_table') {
                        // Create our data table out of JSON data loaded from server.
                        var data = google.visualization.arrayToDataTable(object);
                        var chart = new google.visualization.PieChart(document.getElementById(i));
                        chart.draw(data, {
                            title: i.substr(0, i.length - '_table'.length).toUpperCase(), 
                            width: 450, 
                            height: 270
                        });
                    }
                    else {
                        var data = new google.visualization.DataTable();
                        // transform django date into datetime and django float into number
                        for (var j = 0; j < object.length; ++j) {
                            object[j][0] = new Date(object[j][0]);
                            object[j][1] = parseInt(object[j][1]);
                        }

                        data.addColumn('datetime', 'Date added');
                        data.addColumn('number', 'Price');
                        data.addColumn({type: 'string', role: 'annotation'});
                        data.addColumn({type: 'string', role: 'annotationText'});
                        data.addRows(object);

                        var options = {
                            title: i.substr(0, i.length - '_table'.length).toUpperCase(),
                            width: 500, 
                            height: 300
                        };

                        var chart = new google.visualization.LineChart(document.getElementById(i));
                        chart.draw(data, options);
                    }
                });
            }
        },
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