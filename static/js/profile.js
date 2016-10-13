var exp_height = $('#profile .exp .content p').height() + 25;
$(window).load(function(){
	$('#profile #sidebar').height($('#challenger_profile').height());

	if(exp_height > 100){
	    $('#profile .exp').height(exp_height);
	    $('#profile .exp .title').height(exp_height);
	}
});
$(window).on('resize', function(){
    if(exp_height > 100){
	    $('#profile .exp').height(exp_height);
	    $('#profile .exp .title').height(exp_height);
	}
});