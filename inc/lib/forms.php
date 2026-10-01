<?php

/**
 * Forms: Contact Form 7 (free, installed through TGMPA) renders the contact form and the footer sign-up.
 * The plugin's own stylesheet is switched off; the theme styles the forms with its tokens (.form, .newsletter__form).
 */
add_filter( 'wpcf7_load_css', '__return_false' );
add_filter( 'wpcf7_autop_or_not', '__return_false' );

// Club settings value (a shortcode or just the form number) to rendered form HTML. '' when empty or the plugin is off.
function tvbc_form( $value ) {
	$value = trim( (string) $value );
	if ( '' === $value || ! shortcode_exists( 'contact-form-7' ) ) {
		return '';
	}
	if ( preg_match( '/^[0-9a-f]{7}$|^\d+$/', $value ) ) {
		$value = '[contact-form-7 id="' . $value . '"]';
	}
	if ( ! preg_match( '/^\[contact-form-7\s[^\]]*\]$/', $value ) ) {
		return '';
	}
	return do_shortcode( $value );
}

?>
