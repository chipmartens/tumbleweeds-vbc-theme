<?php

/**
 * Advanced Custom Fields setup (Secure Custom Fields or ACF Pro)
 */

// Local JSON: field groups live in acf-json/ so they travel with the theme
add_filter( 'acf/settings/save_json', function () {
	return get_template_directory() . '/acf-json';
} );
add_filter( 'acf/settings/load_json', function ( $paths ) {
	$paths[] = get_template_directory() . '/acf-json';
	return $paths;
} );

// Club settings options page (site-wide fields: top bar, info session, footer, helpline, socials)
add_action( 'acf/init', function () {
	if ( function_exists( 'acf_add_options_page' ) && ( ! function_exists( 'acf_get_options_page' ) || ! acf_get_options_page( 'club-settings' ) ) ) {
		acf_add_options_page( array(
			'page_title' => 'Club settings',
			'menu_title' => 'Club settings',
			'menu_slug'  => 'club-settings',
			'capability' => 'edit_posts',
			'icon_url'   => 'dashicons-admin-generic',
			'position'   => 20,
		) );
	}
} );

// Customize WYSIWYG Toolbars
add_filter( 'acf/fields/wysiwyg/toolbars', 'my_toolbars' );
function my_toolbars( $toolbars ) {
	// "Minimal": bold, italic, link, bullet list. Enough for a club volunteer, nothing that can break the layout.
	$toolbars['Minimal']    = array();
	$toolbars['Minimal'][1] = array( 'bold', 'italic', 'link', 'bullist' );
	return $toolbars;
}

// Settings value from the Club settings page ('' when the fields plugin is not active)
function tvbc_opt( $name ) {
	return function_exists( 'get_field' ) ? get_field( $name, 'option' ) : '';
}

// The post ID that holds the flexible content for this request (the posts page when on News)
function tvbc_context_id() {
	if ( is_home() ) {
		return (int) get_option( 'page_for_posts' );
	}
	return (int) get_queried_object_id();
}

// Announcement bar: array( text, link ) when it should show today, else null. Dates are optional.
function tvbc_announcement() {
	static $cache = false;
	if ( false !== $cache ) {
		return $cache;
	}
	$cache = null;
	if ( ! function_exists( 'get_field' ) || ! tvbc_opt( 'announcement_show' ) ) {
		return $cache;
	}
	$text = trim( (string) tvbc_opt( 'announcement_text' ) );
	if ( '' === $text ) {
		return $cache;
	}
	$today = current_time( 'Ymd' );
	$from  = tvbc_opt( 'announcement_from' );
	$until = tvbc_opt( 'announcement_until' );
	if ( ( $from && $today < $from ) || ( $until && $today > $until ) ) {
		return $cache;
	}
	$cache = array( 'text' => $text, 'link' => tvbc_opt( 'announcement_link' ) );
	return $cache;
}

// Info session from Club settings: array when set and not yet over, else null (the rows that use it then disappear)
function tvbc_info_session() {
	$d = tvbc_opt( 'info_date' );
	if ( ! $d || current_time( 'Ymd' ) > $d ) {
		return null;
	}
	$dt = DateTime::createFromFormat( 'Ymd', $d, wp_timezone() );
	if ( ! $dt ) {
		return null;
	}
	return array(
		'title'   => tvbc_opt( 'info_title' ) ?: 'Parent info session',
		'short'   => wp_date( 'D, M j', $dt->getTimestamp() ),
		'long'    => wp_date( 'l, F j', $dt->getTimestamp() ),
		'time'    => (string) tvbc_opt( 'info_time' ),
		'place'   => (string) tvbc_opt( 'info_place' ),
		'details' => (string) tvbc_opt( 'info_details' ),
	);
}

// "1-888-83SPORT (77678)" to array( '1-888-83SPORT', '(77678)' )
function tvbc_phone_parts( $s ) {
	if ( preg_match( '/^(.*?)\s*(\(.*\))\s*$/', (string) $s, $m ) ) {
		return array( $m[1], $m[2] );
	}
	return array( (string) $s, '' );
}

?>
