<?php
// ACF / Secure Custom Fields: local JSON lives in acf-json/, the club settings page, and a loud notice if no fields plugin is active.

add_filter( 'acf/settings/save_json', function () {
	return get_template_directory() . '/acf-json';
} );
add_filter( 'acf/settings/load_json', function ( $paths ) {
	$paths[] = get_template_directory() . '/acf-json';
	return $paths;
} );

add_action( 'acf/init', function () {
	if ( function_exists( 'acf_add_options_page' ) ) {
		acf_add_options_page( array(
			'page_title' => 'Club settings',
			'menu_title' => 'Club settings',
			'menu_slug'  => 'club-settings',
			'capability' => 'edit_pages',
			'icon_url'   => 'dashicons-admin-generic',
			'position'   => 20,
		) );
	}
} );

add_action( 'admin_notices', function () {
	if ( ! function_exists( 'get_field' ) ) {
		echo '<div class="notice notice-error"><p><strong>Tumbleweeds theme:</strong> install and activate <em>Secure Custom Fields</em> (free) or ACF Pro. Page content is edited through its fields.</p></div>';
	}
} );
