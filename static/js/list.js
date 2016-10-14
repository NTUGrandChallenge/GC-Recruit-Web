$(window).load(function(){
	if($('#challenger_list') && ($('#list #sidebar').height() < $('#challenger_list').height())){
		$('#list #sidebar').height($('#challenger_list').height());
	}
	else if($('#team_list') && ($('#list #sidebar').height() < $('#team_list').height())){
		$('#list #sidebar').height($('#team_list').height());
	}
});
