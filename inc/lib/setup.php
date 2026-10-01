<?php
// Theme setup: supports, menus, assets.

add_action( 'after_setup_theme', function () {
	add_theme_support( 'title-tag' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'html5', array( 'search-form', 'gallery', 'caption', 'style', 'script' ) );
	register_nav_menus( array(
		'primary' => 'Primary menu',
		'footer'  => 'Footer menu',
	) );
} );

add_action( 'wp_enqueue_scripts', function () {
	$dir = get_template_directory();
	$uri = get_template_directory_uri();
	wp_enqueue_style( 'tvbc-app', $uri . '/assets/css/app.min.css', array(), filemtime( $dir . '/assets/css/app.min.css' ) );
	wp_enqueue_script( 'tvbc-nav', $uri . '/assets/js/nav.js', array(), filemtime( $dir . '/assets/js/nav.js' ), true );
} );

// Classic Editor everywhere (the plugin is the normal route; this is the fallback).
add_filter( 'use_block_editor_for_post_type', '__return_false', 100 );

// Quiet head: no emoji script, no generator tag, no wp-embed.
remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
remove_action( 'wp_print_styles', 'print_emoji_styles' );
remove_action( 'wp_head', 'wp_generator' );
remove_action( 'wp_head', 'wp_oembed_add_discovery_links' );
remove_action( 'wp_head', 'rest_output_link_wp_head' );
add_action( 'wp_enqueue_scripts', function () {
	wp_dequeue_style( 'wp-block-library' );
	wp_dequeue_style( 'global-styles' );
	wp_dequeue_style( 'classic-theme-styles' );
}, 100 );

// Comments are off: this is a club site, not a blog community.
add_filter( 'comments_open', '__return_false', 20 );
add_filter( 'pings_open', '__return_false', 20 );
