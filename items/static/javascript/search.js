$(document).ready(function(){
	var thread = null;
	var item = null; 
	function getSimilarItems(t){
		if (t == "") {
			return;
		}

		$.ajax({
			type: 'GET',
			url: '/items/search',
			data: {'text': t},
			dataType:'json',
			success: function(data, textStatus, jqXHR){
				if (data.length == 0) {
					$('div#similar_items').hide();
				}
				else {
					console.log(data);
					// clear the list
					$('p#similar_item').remove();
					$.each(data, function(i, item_obj){
						item = '<p id="similar_item"><a href="/items/' + item_obj.pk + '">' + item_obj.fields.name + '</a></p>';
						console.log(item);
						// append template to '#similar_items' div-box
						$('div#similar_items').append(item);
					});
					// display 'similar_items' div-box
					$('div#similar_items').show();
				}
			}
		});
	}

	$('#id_name').keyup(function(){
		clearTimeout(thread);
		var $this = $(this);
		thread = setTimeout(function(){
			getSimilarItems($this.val());
		}, 1000);
	})
})