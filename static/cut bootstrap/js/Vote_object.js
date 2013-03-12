function Vote($this) {
	var prev_vote = $this.siblings('.unvote');
	var revote = prev_vote.length == 1;

	function vote() {
		var data_to_send = {'vote_type': $this.attr('type-id')}
		if (revote) {
			data_to_send.revote = true;
		}
		$.ajax({
			data: data_to_send,
			type: 'post',
			url: '/feedbacks/' + $this.parents('li').attr('feedback-id') + '/vote/',
			dataType: 'json'
		}).done(function(data, textStatus, jqXHR) {
			affect_score(parseInt($this.attr('weight')));
			affect_count(1);
			change_class_to('.unvote');
		}).fail(function(jqXHR, textStatus, errorThrown) {
			alert(jqXHR.responseText);
		});
	}

	function unvote() {
		$.ajax({
            data: {'vote_type': $this.attr('type-id')},
            type: 'post',
            url: '/feedbacks/' + $this.parents('li').attr('feedback-id') + '/unvote/',
            dataType: 'json'
        }).done(function(data, textStatus, jqXHR) {
        	affect_score(parseInt($this.attr('weight')));
        	affect_count(-1);
        	change_class_to('.vote');
        }.fail(function(jqXHR, textStatus, errorThrown) {
			alert(jqXHR.responseText);
		});
	}

	function affect_score(weight) {
		var score = $this.parent().prev('span');
		score.text(parseInt(score.text) + weight);
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
		if (state == '.vote') {
			return '.unvote';
		else
			return '.vote';
	}

	return {
		vote: vote,
		unvote: unvote
	}
}