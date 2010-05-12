$(function() {
	// add hover effect for IE6
	if($.browser.msie && $.browser.version < 7) {
		$('#jobs tbody tr').hover(function() {
			$(this).css('background-color', '#eee');
		}, function() {
			$(this).css('background-color', 'transparent');
		});
	}
	
	// add pointer cursor and click event to tr 
	$('#jobs tbody tr').css('cursor', 'pointer').click(function() {
		var winLoc = $(this).children('td').children('a:first').attr('href');
		window.location.href = winLoc;
	});
});