$(window).load(function(){
	if($('#team_profile #sidebar').height() < $('#team_info').height()){
		$('#team_profile #sidebar').height($('#team_info').height());
	}
});