var fullTextSearch = {
	config: {
		formId: "someid",
		timeout: 1000,
		url: '#',
		resultsHandler: function(data, textStatus, jqXHR){
			console.log(data);
			alert("We've got some server data!");
		}
	},
	init: function(config){
		$.extend(this.config, config);
		var thread = null;
		$(this.config.formId).keyup(function(){
			clearTimeout(thread);
			var $this = $(this);
			thread = setTimeout(function(){
				this.search($this.val());
			}, this.config.timeout);
		});
	},
	search: function(query){
		$.ajax({
			type: 'GET',
			url: this.config.url,
			data: {'query': query},
			dataType:'json',
			success: this.config.searchHandler
		});
	}
}