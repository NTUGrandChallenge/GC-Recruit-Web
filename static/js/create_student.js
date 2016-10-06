$('#create_student .interest .logo-wrapper').hover(function(){
	$(this).children('.highlight').css('visibility', 'visible');
	$('#create_student .interest .description p').css('visibility', 'hidden');
	$('#create_student .interest .description p:nth-child(' + ($(this).parent().index() + 1) + ')').css('visibility', 'visible');
},function(){
	$(this).children('.highlight').css('visibility', '');
	$('#create_student .interest .description p').css('visibility', '');
});
$('#create_student .interest .logo-wrapper').on('click', function(){
	// $('#create_student .interest input[name="interest"]').prop('checked', false);
	$('#create_student .interest input[name="interest"]:nth-child(' + ($(this).parent().index() + 1) + ')').prop('checked', true);
	
	$('#create_student .interest .logo-wrapper .highlight').removeClass('locked');
	$(this).children('.highlight').addClass('locked');
	$('#create_student .interest .description p').removeClass('locked');
	$('#create_student .interest .description p:nth-child(' + ($(this).parent().index() + 1) + ')').addClass('locked');
})


$('#create_student .one-talent .add-talent').on('click', function(){
	$(this).parents('.one-talent').next('.one-talent').css('display', 'block');
	$(this).css('display', 'none');
});
