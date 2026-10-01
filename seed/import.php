<?php
/**
 * Seed import for the Tumbleweeds theme. Re-runnable: pages, coaches, posts and images are matched and rewritten.
 *
 *   wp eval-file wp-content/themes/tumbleweeds-vbc/seed/import.php
 *
 * Needs the theme active and Secure Custom Fields (or ACF Pro) active. Reads seed/content.json (written by
 * tools/build_seed.py). Changes only this site's content: never touches users or plugins.
 * Safety: refuses to run when the site is not a fresh or staging copy unless TVBC_SEED_FORCE is defined.
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
if ( ! function_exists( 'update_field' ) ) {
	wp_die( 'Activate Secure Custom Fields (or ACF Pro) first.' );
}
require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/media.php';
require_once ABSPATH . 'wp-admin/includes/image.php';

$theme = get_stylesheet_directory();
$data  = json_decode( file_get_contents( $theme . '/seed/content.json' ), true );
$home  = trailingslashit( home_url( '/' ) );
$say   = function ( $m ) { if ( class_exists( 'WP_CLI' ) ) { WP_CLI::log( $m ); } else { echo $m . "\n"; } };

/* 1. Images -> media library (matched by _tvbc_seed meta) */
$img = array();
foreach ( $data['images'] as $key => $spec ) {
	$found = get_posts( array( 'post_type' => 'attachment', 'meta_key' => '_tvbc_seed', 'meta_value' => $key, 'posts_per_page' => 1, 'fields' => 'ids', 'post_status' => 'any' ) );
	if ( $found ) {
		$img[ $key ] = (int) $found[0];
		continue;
	}
	$src = $theme . '/' . $spec['file'];
	$tmp = wp_tempnam( basename( $src ) );
	copy( $src, $tmp );
	$id = media_handle_sideload( array( 'name' => basename( $src ), 'tmp_name' => $tmp ), 0 );
	if ( is_wp_error( $id ) ) {
		$say( 'image failed: ' . $key . ' ' . $id->get_error_message() );
		continue;
	}
	update_post_meta( $id, '_tvbc_seed', $key );
	update_post_meta( $id, '_wp_attachment_image_alt', $spec['alt'] );
	$img[ $key ] = (int) $id;
	$say( "image: $key -> $id" );
}

/* Helpers */
$upsert = function ( $type, $slug, $args ) {
	$existing = get_posts( array( 'post_type' => $type, 'name' => $slug, 'post_status' => 'any', 'posts_per_page' => 1, 'fields' => 'ids' ) );
	$args     = array_merge( array( 'post_type' => $type, 'post_name' => $slug, 'post_status' => 'publish' ), $args );
	if ( $existing ) {
		$args['ID'] = $existing[0];
		return wp_update_post( $args );
	}
	return wp_insert_post( $args );
};

/* 2. Pages first (empty), so links and the coaches-page setting can point at real IDs */
$page_ids = array();
foreach ( $data['pages'] as $p ) {
	$page_ids[ $p['slug'] ] = $upsert( 'page', $p['slug'], array( 'post_title' => $p['title'], 'post_content' => '' ) );
}

$form_codes = array();
$resolve = function ( $v, $k = '' ) use ( &$resolve, &$img, &$page_ids, &$form_codes, $home ) {
	if ( is_array( $v ) ) {
		$o = array();
		foreach ( $v as $kk => $vv ) {
			$o[ $kk ] = $resolve( $vv, is_string( $kk ) ? $kk : $k );
		}
		// a {title,url} pair is an ACF link
		if ( isset( $o['title'], $o['url'] ) && 2 === count( $o ) ) {
			$o['target'] = '';
		}
		return $o;
	}
	if ( is_string( $v ) ) {
		if ( 0 === strpos( $v, '@img:' ) ) {
			return $img[ substr( $v, 5 ) ] ?? 0;
		}
		if ( 0 === strpos( $v, '@form:' ) ) {
			return $form_codes[ substr( $v, 6 ) ] ?? '';
		}
		if ( 0 === strpos( $v, '@page:' ) ) {
			return $page_ids[ substr( $v, 6 ) ] ?? 0;
		}
		return str_replace( '{home}', $home, $v );
	}
	return $v;
};

// Which field-key prefix a top-level field belongs to, for a given kind of post
$prefix = function ( $kind, $name ) {
	if ( 0 === strpos( $name, 'band_' ) ) {
		return 'field_tvbc_band_';
	}
	if ( 'page' === $kind ) {
		return 'field_tvbc_hero_';
	}
	if ( 'coach' === $kind ) {
		return 'field_tvbc_coach_';
	}
	return 'field_tvbc_news_';
};

/* 2b. Contact Form 7 forms (only when the plugin is active). Club settings holds each form's shortcode. */
if ( class_exists( 'WPCF7_ContactForm' ) ) {
	foreach ( $data['forms'] as $key => $spec ) {
		$found = get_posts( array( 'post_type' => 'wpcf7_contact_form', 'title' => $spec['title'], 'post_status' => 'any', 'posts_per_page' => 1, 'fields' => 'ids' ) );
		$cf    = $found ? wpcf7_contact_form( $found[0] ) : WPCF7_ContactForm::get_template( array( 'title' => $spec['title'], 'locale' => 'en_US' ) );
		$mail  = array_merge( $cf->prop( 'mail' ), array(
			'subject'            => $spec['subject'],
			'sender'             => 'Tumbleweeds website <wordpress@tumbleweedsvolleyball.com>',
			'recipient'          => $spec['to'],
			'body'               => $spec['body'],
			'additional_headers' => 'Reply-To: [your-email]',
		) );
		$cf->set_properties( array( 'form' => $spec['form'], 'mail' => $mail ) );
		$cf->save();
		$form_codes[ $key ] = $cf->shortcode();
		$say( "form: $key -> " . $form_codes[ $key ] );
	}
}
$set_seo = function ( $id, $seo ) {
	if ( $seo ) {
		update_post_meta( $id, '_yoast_wpseo_title', $seo['title'] );
		update_post_meta( $id, '_yoast_wpseo_metadesc', $seo['desc'] );
	}
};

foreach ( $data['pages'] as $p ) {
	$id = $page_ids[ $p['slug'] ];
	$set_seo( $id, $p['seo'] ?? null );
	foreach ( $resolve( $p['hero'] ) as $name => $val ) {
		update_field( $prefix( 'page', $name ) . $name, $val, $id );
	}
	update_field( 'field_tvbc_page_flex_content', $resolve( $p['flex'] ), $id );
	if ( ! empty( $p['front_page'] ) ) {
		update_option( 'show_on_front', 'page' );
		update_option( 'page_on_front', $id );
	}
	if ( ! empty( $p['posts_page'] ) ) {
		update_option( 'page_for_posts', $id );
	}
	$say( "page: {$p['slug']} -> $id" );
}

/* 3. Coaches */
$coach_ids = array();
foreach ( $data['coaches'] as $c ) {
	$id = $upsert( 'coach', $c['slug'], array( 'post_title' => $c['title'], 'menu_order' => $c['menu_order'] ) );
	$coach_ids[ $c['slug'] ] = $id;
	$set_seo( $id, $c['seo'] ?? null );
	foreach ( $resolve( $c['fields'] ) as $name => $val ) {
		update_field( $prefix( 'coach', $name ) . $name, $val, $id );
	}
	$say( "coach: {$c['slug']} -> $id" );
}

/* 4. News posts */
foreach ( $data['posts'] as $po ) {
	$id = $upsert( 'post', $po['slug'], array( 'post_title' => $po['title'], 'post_content' => $po['content'], 'post_excerpt' => $po['excerpt'], 'post_date' => $po['date'], 'post_date_gmt' => get_gmt_from_date( $po['date'] ) ) );
	set_post_thumbnail( $id, $img[ $po['thumb'] ] );
	$set_seo( $id, $po['seo'] ?? null );
	foreach ( $resolve( $po['fields'] ) as $name => $val ) {
		update_field( $prefix( 'post', $name ) . $name, $val, $id );
	}
	$say( "post: {$po['slug']} -> $id" );
}
foreach ( array( 'hello-world' => 'post', 'sample-page' => 'page' ) as $slug => $type ) {
	foreach ( get_posts( array( 'post_type' => $type, 'name' => $slug, 'post_status' => 'any', 'posts_per_page' => 1, 'fields' => 'ids' ) ) as $del ) {
		wp_delete_post( $del, true );
	}
}

/* 5. Club settings (the options page) */
foreach ( $resolve( $data['settings'] ) as $name => $val ) {
	update_field( 'field_tvbc_set_' . $name, $val, 'option' );
}
$say( 'settings -> Club settings' );

/* 5b. Privacy policy page (WordPress Settings, Privacy points at it; the footer link uses that) and Yoast SEO defaults */
if ( isset( $page_ids['privacy-policy'] ) ) {
	update_option( 'wp_page_for_privacy_policy', $page_ids['privacy-policy'] );
}
if ( class_exists( 'WPSEO_Options' ) ) {
	WPSEO_Options::set( 'company_or_person', 'company' );
	WPSEO_Options::set( 'company_name', 'Tumbleweeds Volleyball Club' );
	WPSEO_Options::set( 'website_name', 'Tumbleweeds Volleyball Club' );
	WPSEO_Options::set( 'opengraph', true );
	WPSEO_Options::set( 'twitter', true );
	if ( ! empty( $img['og'] ) ) {
		WPSEO_Options::set( 'og_default_image', wp_get_attachment_url( $img['og'] ) );
		WPSEO_Options::set( 'og_default_image_id', $img['og'] );
	}
	WPSEO_Options::set( 'show_onboarding_notice', false );
	WPSEO_Options::set( 'dismiss_configuration_workout_notice', true );
	$say( 'Yoast SEO defaults set' );
}

/* 6. Menus: Header Menu and Footer Menu (Appearance, Menus) */
$make_menu = function ( $name, $items ) use ( $page_ids ) {
	$menu = wp_get_nav_menu_object( $name );
	$mid  = $menu ? $menu->term_id : wp_create_nav_menu( $name );
	foreach ( (array) wp_get_nav_menu_items( $mid ) as $item ) {
		wp_delete_post( $item->ID, true );
	}
	foreach ( $items as $slug => $label ) {
		wp_update_nav_menu_item( $mid, 0, array( 'menu-item-title' => $label, 'menu-item-object' => 'page', 'menu-item-object-id' => $page_ids[ $slug ], 'menu-item-type' => 'post_type', 'menu-item-status' => 'publish' ) );
	}
	return $mid;
};
$header_items = array();
$footer_items = array();
foreach ( $data['pages'] as $p ) {
	if ( ! empty( $p['menu'] ) ) {
		$header_items[ $p['slug'] ] = $p['menu'];
	}
	$footer_label = array_key_exists( 'footer_menu', $p ) ? $p['footer_menu'] : ( $p['menu'] ?? '' );
	if ( $footer_label ) {
		$footer_items[ $p['slug'] ] = $footer_label;
	}
}
set_theme_mod( 'nav_menu_locations', array(
	'header-menu' => $make_menu( 'Header Menu', $header_items ),
	'footer-menu' => $make_menu( 'Footer Menu', $footer_items ),
) );

/* 7. Site options. blog_public 0: this is a staging copy, keep it out of search. */
update_option( 'blogname', 'Tumbleweeds Volleyball Club' );
update_option( 'blogdescription', 'Kamloops youth volleyball. Developing athletes from the ground up.' );
update_option( 'timezone_string', 'America/Vancouver' );
update_option( 'blog_public', 0 );
update_option( 'default_comment_status', 'closed' );
update_option( 'uploads_use_yearmonth_folders', 1 );
global $wp_rewrite;
$wp_rewrite->set_permalink_structure( '/%postname%/' );
flush_rewrite_rules();
$say( 'done' );
