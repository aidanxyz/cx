$(document).ready(function(){
	
	$('form#feedback').submit(function(){
		var form = $(this);
		$.ajax({
			data: $(this).serialize(),
			type: $(this).attr('method'),
			url:  $(this).attr('action'),
			dataType: 'json',
			success: function(data, textStatus, jqXHR) {
				var feedback = ich.feedback(data);
				form.before(feedback);
			}
		});
		return false;
	});
});