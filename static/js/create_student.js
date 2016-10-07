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
	// $('#create_student .interest input[name="interest"]').prop('checked', false);
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
	// $(this).parents('.one-talent').find('.group select').css('display', 'none').find('select').attr('name', 'groupX');
	// $(this).parents('.one-talent').find('.bootstrap-select.son-of-c-' + ($(this).find(':selected').attr('data-id'))).css('display', 'inherit')
	// .find('select').attr('name', 'group').find('option:first-child').attr('selected', true);
	console.log($(this).find(':selected').text());
});
$('#create_student .one-talent .group select').change(function(){
	$(this).parents('.one-talent').find('.talent select option').css('display', 'none');
	$(this).parents('.one-talent').find('.talent select option.son-of-g-' + $(this).find(':selected').attr('data-id')).css('display', 'inherit').first().prop('selected', 'true');
// 	console.log("GG");
// 	$(this).parents('.one-talent').find('.talent .bootstrap-select').css('display', 'none').find('select').attr('name', 'talentX');
// 	$(this).parents('.one-talent').find('.bootstrap-select.son-of-g-' + ($(this).find(':selected').attr('data-id'))).css('display', 'inherit')
// 	.find('select').attr('name', 'talent[]').find('option:nth-child(1)').attr('selected', true);
});
$('#create_student .one-talent select[name="talent[]"]').change(function(){
	$(this).parents('.one-talent').find('.add-talent').css('display', 'initial');
});

// add talent
$('#create_student .one-talent .add-talent').on('click', function(){
	$(this).parents('.one-talent').next('.one-talent').css('display', 'block');
	$(this).css('display', 'none');
});


$(document).ready(function(){
	$('#create_student .interest input[name="interest"]:nth-child(1)').prop('checked', true);
	$('#create_student .role .radio-area:first-child input').prop('checked', true);
})