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

// Flexible content: show each section's heading in its title bar, and start with the sections closed so a long page is a short list
add_filter( 'acf/fields/flexible_content/layout_title/name=flex_content', 'tvbc_layout_title', 10, 4 );
function tvbc_layout_title( $title, $field, $layout, $i ) {
	$text = get_sub_field( 'section_heading' ) ?: ( get_sub_field( 'band_heading' ) ?: get_sub_field( 'section_eyebrow' ) );
	return $text ? $title . ': <span class="tvbc-layout-preview">' . esc_html( wp_trim_words( $text, 8, '...' ) ) . '</span>' : $title;
}
add_action( 'admin_footer', function () {
	$screen = get_current_screen();
	if ( ! $screen || 'page' !== $screen->post_type ) {
		return;
	}
	echo '<style>.tvbc-layout-preview{font-weight:400;opacity:.75}</style>';
	echo '<script>if(window.acf){acf.addAction("ready",function(){jQuery(".acf-flexible-content .layout").each(function(){acf.getInstance&&jQuery(this).addClass("-collapsed")})})}</script>';
} );

// Settings value from the Club settings page ('' when the fields plugin is not active)
function tvbc_opt( $name ) {
	return function_exists( 'get_field' ) ? get_field( $name, 'option' ) : '';
}

// Small wording from Club settings with the built-in text as the default
function tvbc_label( $name, $default ) {
	$v = trim( (string) tvbc_opt( $name ) );
	return '' !== $v ? $v : $default;
}

// Registration link from Club settings as an ACF-style link array, or null until the club has one
function tvbc_registration() {
	$url = trim( (string) tvbc_opt( 'registration_url' ) );
	if ( '' === $url ) {
		return null;
	}
	return array( 'url' => $url, 'title' => tvbc_label( 'registration_label', 'Register now' ), 'target' => '_blank' );
}

// $use true and a registration link set: the registration link, else the button's own link
function tvbc_or_registration( $link, $use ) {
	$reg = $use ? tvbc_registration() : null;
	return $reg ? $reg : $link;
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
