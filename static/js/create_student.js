// interest
$('#create_student .interest .logo-wrapper').hover(function(){
	$(this).children('.highlight').css('visibility', 'visible');
	$('#create_student .interest .description p').css('visibility', 'hidden');
	$('#create_student .interest .description p:nth-child(' + ($(this).parent().index() + 1) + ')').css('visibility', 'visible');
},function(){
	$(this).children('.highlight').css('visibility', '');
	$('#create_student .interest .description p').css('visibility', '');
});
$('#create_student .interest .logo-wrapper').on('click', function(){
	$('#create_student .interest input[name="interest"]:nth-child(' + ($(this).parent().index() + 2) + ')').prop('checked', true);
	$('#create_student .interest .logo-wrapper .highlight').removeClass('locked');
	$(this).children('.highlight').addClass('locked');
	$('#create_student .interest .description p').removeClass('locked');
	$('#create_student .interest .description p:nth-child(' + ($(this).parent().index() + 1) + ')').addClass('locked');
})

// talent cascading
$('#create_student .one-talent .category select').change(function(){
	$(this).parents('.one-talent').find('.group select option').css('display', 'none');
	$(this).parents('.one-talent').find('.group select option.son-of-c-' + $(this).find(':selected').attr('data-id')).css('display', 'inherit').first().prop('selected', 'true');
	$(this).parents('.one-talent').find('.group select').trigger('change');
});
$('#create_student .one-talent .group select').change(function(){
	$(this).parents('.one-talent').find('.talent select option').css('display', 'none');
	$(this).parents('.one-talent').find('.talent select option.son-of-g-' + $(this).find(':selected').attr('data-id')).css('display', 'inherit').first().prop('selected', 'true');
});

// add talent
$('#create_student .one-talent .add-talent').on('click', function(){
	$(this).parents('.one-talent').next('.one-talent').removeClass('hide')
	$(this).addClass('hide');
});


$(document).ready(function(){
	$('#create_student .interest .col-xs-5ths:nth-child(' + $('#create_student .interest input[name="interest"]:checked').index() + ') .highlight').addClass('locked');
	$('#create_student .interest .description p:nth-child(' + $('#create_student .interest input[name="interest"]:checked').index() + ')').addClass('locked');
})