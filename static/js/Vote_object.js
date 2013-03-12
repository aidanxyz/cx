authenticated: {
    used: function() {
        // adding feedback
        $('form#add_feedback').submit(function(){
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
    },
    not_used: function() {
        // <I used it> click
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
        });
        // voting, unvoting, adding a feedback on unused state
        $('.vote, .unvote, a#add_feedback').click(function() {
            $('#not_used-modal').modal();
        });
    }
},