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
$('#create_student .one-talent select[name="category"]').change(function(){
	$(this).parents('.one-talent').find('.group .bootstrap-select').css('display', 'none').find('select').attr('name', 'XXX');
	$(this).parents('.one-talent').find('.bootstrap-select.son-of-c-' + ($(this).find(':selected').attr('data-id'))).css('display', 'inherit').find('select').attr('name', 'group');
	console.log('.son-of-c-' + ($(this).find(':selected').index()+1));
});
$('#create_student .one-talent select[name="group"]').change(function(){
	$(this).parents('.one-talent').find('.talent .bootstrap-select').css('display', 'none').find('select').attr('name', 'XXX');
	$(this).parents('.one-talent').find('.bootstrap-select.son-of-g-' + ($(this).find(':selected').attr('data-id'))).css('display', 'inherit').find('select').attr('name', 'talent[]');
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