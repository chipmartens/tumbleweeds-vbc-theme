<?php
/**
 * Seed import for the Tumbleweeds theme. Re-runnable: pages, coaches and posts are matched by slug and rewritten.
 *
 *   wp eval-file wp-content/themes/tumbleweeds-vbc/seed/import.php
 *
 * Needs the theme active and Secure Custom Fields (or ACF Pro) active. Reads seed/content.json.
 * Changes only this site's content. Never touches users, plugins, or anything outside the seed.
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

/* Helpers: resolve @img:, @coach:, {home}, and bare strings under link keys */
$coach_ids = array();
$resolve   = function ( $v, $k = '' ) use ( &$resolve, &$img, &$coach_ids, $home ) {
	if ( is_array( $v ) ) {
		$o = array();
		foreach ( $v as $kk => $vv ) {
			$o[ $kk ] = $resolve( $vv, is_string( $kk ) ? $kk : $k );
		}
		return $o;
	}
	if ( is_string( $v ) ) {
		if ( 0 === strpos( $v, '@img:' ) ) {
			return $img[ substr( $v, 5 ) ] ?? 0;
		}
		if ( 0 === strpos( $v, '@coach:' ) ) {
			return $coach_ids[ substr( $v, 7 ) ] ?? 0;
		}
		$v = str_replace( '{home}', $home, $v );
		if ( in_array( $k, array( 'link', 'button_link', 'header_cta_link' ), true ) && '' !== $v ) {
			return array( 'title' => '', 'url' => $v, 'target' => '' );
		}
	}
	return $v;
};
$upsert = function ( $type, $slug, $args ) {
	$existing = get_posts( array( 'post_type' => $type, 'name' => $slug, 'post_status' => 'any', 'posts_per_page' => 1, 'fields' => 'ids' ) );
	$args     = array_merge( array( 'post_type' => $type, 'post_name' => $slug, 'post_status' => 'publish' ), $args );
	if ( $existing ) {
		$args['ID'] = $existing[0];
		return wp_update_post( $args );
	}
	return wp_insert_post( $args );
};

/* 2. Coaches */
foreach ( $data['coaches'] as $c ) {
	$id = $upsert( 'coach', $c['slug'], array( 'post_title' => $c['title'], 'menu_order' => $c['menu_order'] ) );
	$coach_ids[ $c['slug'] ] = $id;
	foreach ( $resolve( $c['fields'] ) as $name => $val ) {
		update_field( 'field_tvbc_coach_' . $name, $val, $id );
	}
	$say( "coach: {$c['slug']} -> $id" );
}

/* 3. Pages */
$page_ids = array();
foreach ( $data['pages'] as $p ) {
	$id = $upsert( 'page', $p['slug'], array( 'post_title' => $p['title'], 'post_content' => '' ) );
	$page_ids[ $p['slug'] ] = $id;
	foreach ( $resolve( $p['hero'] ) as $name => $val ) {
		update_field( 'field_tvbc_page_' . $name, $val, $id );
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

/* 4. News posts */
foreach ( $data['posts'] as $po ) {
	$id = $upsert( 'post', $po['slug'], array( 'post_title' => $po['title'], 'post_content' => $po['content'], 'post_date' => $po['date'], 'post_date_gmt' => get_gmt_from_date( $po['date'] ) ) );
	$say( "post: {$po['slug']} -> $id" );
}
foreach ( array( 'hello-world' => 'post', 'sample-page' => 'page' ) as $slug => $type ) {
	foreach ( get_posts( array( 'post_type' => $type, 'name' => $slug, 'posts_per_page' => 1, 'fields' => 'ids' ) ) as $del ) {
		wp_delete_post( $del, true );
	}
}

/* 5. Club settings: the options page when it exists, else the front page */
$target = function_exists( 'acf_add_options_page' ) ? 'option' : (int) get_option( 'page_on_front' );
foreach ( $resolve( $data['settings'] ) as $name => $val ) {
	update_field( 'field_tvbc_set_' . $name, $val, $target );
}
$say( 'settings -> ' . ( 'option' === $target ? 'options page' : 'front page' ) );

/* 6. Menu */
$menu = wp_get_nav_menu_object( 'Primary' );
$mid  = $menu ? $menu->term_id : wp_create_nav_menu( 'Primary' );
foreach ( (array) wp_get_nav_menu_items( $mid ) as $item ) {
	wp_delete_post( $item->ID, true );
}
foreach ( $data['pages'] as $p ) {
	if ( empty( $p['menu'] ) ) {
		continue;
	}
	wp_update_nav_menu_item( $mid, 0, array( 'menu-item-title' => $p['menu'], 'menu-item-object' => 'page', 'menu-item-object-id' => $page_ids[ $p['slug'] ], 'menu-item-type' => 'post_type', 'menu-item-status' => 'publish' ) );
}
set_theme_mod( 'nav_menu_locations', array( 'primary' => $mid, 'footer' => $mid ) );

/* 7. Site options. blog_public 0: this is a staging copy, keep it out of search. */
update_option( 'blogname', 'Tumbleweeds Volleyball Club' );
update_option( 'blogdescription', 'Kamloops youth volleyball. Developing athletes from the ground up.' );
update_option( 'timezone_string', 'America/Vancouver' );
update_option( 'blog_public', 0 );
update_option( 'default_comment_status', 'closed' );
global $wp_rewrite;
$wp_rewrite->set_permalink_structure( '/%postname%/' );
flush_rewrite_rules();
$say( 'done' );
