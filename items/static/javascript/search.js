$(document).ready(function(){
	var thread = null;

	function findMember(t){
		alert(t);
	}

	$('#id_name').keyup(function(){
		clearTimeout(thread);
		var $this = $(this);
		thread = setTimeout(function(){
			findMember($this.val());
		}, 1000);
	})
})