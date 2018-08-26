$(document).ready(function(){
		

		$('#btn-about').click(function(){
			$(this).addClass('btn-success');
			$('#btn-friends').removeClass('btn-success');
			$('.friend-view').delay(100).fadeOut(100);
			$('.about-view').fadeIn(100);

		});

		$('#btn-friends').click(function(){
			$(this).addClass('btn-success');
			$('#btn-about').removeClass('btn-success');
			$('.about-view').delay(100).fadeOut(100);
			$('.friend-view').fadeIn(100);

		});
		
	});