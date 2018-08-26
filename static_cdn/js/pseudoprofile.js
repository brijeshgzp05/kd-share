$(document).ready(function(){
		$('.msg').click(function(){
			var endpoint = "{% url 'message:chat' id=123 %}"
			endpoint = endpoint.replace('123',{{u.profile.id}});
			document.location.href = endpoint
		});
	});