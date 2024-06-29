$(document).ready(function() {
	'use strict';
		// Photo chooser
		function readURL(input) {

		    if (input.files && input.files[0]) {
		        var reader = new FileReader();

		        reader.onload = function (e) {
		        	console.log(e.target.result)
		            $('#photoXXX-photo').css('background-image', 'url(' + e.target.result + ')');
		        }

		        reader.readAsDataURL(input.files[0]);
		    }
		}
		$('#photoXXX').on('change', function() {
			readURL(this)
		});
	    /*================== Date Picker Initialization ===================*/
        $('#input_dateinput').pickadate({
        	format: 'dd/mm/yyyy',
        	today: '',
			clear: '',
			close: ''
        });

        $('#event_time').pickatime({
        	format: 'hh:i'
        });
    /**
     * Scroll
     */
    $(window).scroll(function() {
        if ($(this).scrollTop() > 220) {
            $('.header-sticky').addClass('active');
        } else {
            $('.header-sticky').removeClass('active');
        }
    });

    /**
     * Filter
     */
	$('.filter h2').on('click', function(e) {
		$(this).toggleClass('closed');
	});

    /**
     * Checkbox & radio inputs
     */
    $('input[type=checkbox], input[type=radio]').ezMark();

	/**
	 * Sidenav trigger
	 */
	$('.sidenav-trigger, .sidenav-close, .page-wrapper-overlay').on('click', function(e) {
		e.preventDefault();
		$('body').toggleClass('sidenav-open');
	});
	
	/**
	 * Customizer
	 */	 
	$('.customizer-title').on('click', function() {		
		$('.customizer').toggleClass('open');
	});

	$('.customizer a').click('click', function(e) {
		e.preventDefault();

		var cssFile = $(this).attr('href');
		$('#css-primary').attr('href', cssFile);
	});		
});