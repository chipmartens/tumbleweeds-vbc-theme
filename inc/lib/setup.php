<?php

/**
 * Theme setup
 */
function setup () {
	// Initialize menus
	register_nav_menus( array(
		'header-menu'   => __( 'Header Menu' ),
		'footer-menu'   => __( 'Footer Menu' ),
		'utility-links' => __( 'Utility Links' )
	) );

	// Enable Post Thumbnails
	add_theme_support( 'post-thumbnails' );
	add_image_size( 'hero', 2000, 2000, false );
	add_image_size( 'sheet', 1200, 1200, false );
	add_image_size( 'sheet-sm', 640, 640, false );

	add_filter( 'image_size_names_choose', 'custom_image_sizes' );
	function custom_image_sizes( $sizes ) {
		return array_merge( $sizes, array(
			'hero'     => __( 'Hero' ),
			'sheet'    => __( 'Section photo' ),
			'sheet-sm' => __( 'Section photo small' ),
		) );
	}

	// Enables HTML5 markup for search forms, comment forms, comment lists, gallery, and caption.
	add_theme_support( 'html5', array(
		'search-form',
		'comment-form',
		'comment-list',
		'gallery',
		'caption'
	) );

	// WordPress manages titles
	add_theme_support( 'title-tag' );

	// Style the Classic / TinyMCE editor (incl. ACF WYSIWYG fields) so
	// authors see Figtree and front-end typography while editing.
	add_editor_style( 'assets/css/editor-style.min.css' );
}
add_action( 'after_setup_theme', 'setup' );

function custom_document_title_separator( $sep ) {
	return '|';
}
add_filter( 'document_title_separator', 'custom_document_title_separator', 10, 1 );

/**
 * Plugin activation (TGMPA)
 *
 * Chez Koop bundles the ACF Pro zip in inc/plugins/. This repository is public, so the zip is
 * NOT committed: the fields plugin is Secure Custom Fields from wordpress.org. 'is_callable'
 * marks it satisfied when ACF Pro (or anything that defines the function) is already active.
 */
require_once( get_template_directory() . '/inc/class-tgm-plugin-activation.php' );
add_action( 'tgmpa_register', 'register_required_plugins' );
function register_required_plugins() {
	$plugins = array(
		array(
			'name'        => 'Secure Custom Fields (or ACF Pro)',
			'slug'        => 'secure-custom-fields',
			'required'    => true,
			'is_callable' => 'acf_add_local_field_group',
		),
		array(
			'name'     => 'Classic Editor',
			'slug'     => 'classic-editor',
			'required' => false,
		),
	);

	tgmpa( $plugins, array(
		'id'           => 'tvbc',
		'menu'         => 'tgmpa-install-plugins',
		'has_notices'  => true,
		'dismissable'  => true,
		'is_automatic' => true,
	) );
}

/**
 * Theme assets
 */
function assets() {
	// Queues up stylesheets
	wp_enqueue_style( 'app-style', get_template_directory_uri() . '/assets/css/app.min.css', array(), filemtime( get_template_directory() . '/assets/css/app.min.css' ) );

	// Queues up scripts
	wp_enqueue_script( 'app-script', get_template_directory_uri() . '/dist/js/app.bundle.js', array( 'jquery' ), filemtime( get_template_directory() . '/dist/js/app.bundle.js' ), true );
}
add_action( 'wp_enqueue_scripts', 'assets' );

// Classic Editor everywhere (the plugin is the normal route; this is the fallback).
add_filter( 'use_block_editor_for_post_type', '__return_false', 100 );

// Block-editor styles are not used on the front end.
add_action( 'wp_enqueue_scripts', function () {
	wp_dequeue_style( 'wp-block-library' );
	wp_dequeue_style( 'global-styles' );
	wp_dequeue_style( 'classic-theme-styles' );
}, 100 );

?>
