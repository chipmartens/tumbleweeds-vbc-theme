<?php
/**
 * Register Custom Post Types
 */
function tvbc_register_cpts() {
	// Coach CPT: one post per person, fields in the "Coach Details" ACF group.
	register_post_type( 'coach', array(
		'labels' => array(
			'name'               => __( 'Coaches' ),
			'singular_name'      => __( 'Coach' ),
			'add_new'            => __( 'Add New' ),
			'add_new_item'       => __( 'Add a coach' ),
			'edit_item'          => __( 'Edit coach' ),
			'new_item'           => __( 'New coach' ),
			'view_item'          => __( 'View coach page' ),
			'search_items'       => __( 'Search coaches' ),
			'all_items'          => __( 'All coaches' ),
			'not_found'          => __( 'No coaches found' ),
			'not_found_in_trash' => __( 'No coaches found in Trash' ),
		),
		'public'              => true,
		'exclude_from_search' => false,
		'show_ui'             => true,
		'show_in_menu'        => true,
		'show_in_nav_menus'   => true,
		'menu_icon'           => 'dashicons-groups',
		'menu_position'       => 21,
		'capability_type'     => 'post',
		'hierarchical'        => false,
		'supports'            => array( 'title', 'page-attributes' ), // page-attributes = the Order box
		'has_archive'         => false,
		'rewrite'             => array( 'slug' => 'coaches', 'with_front' => false ),
		'query_var'           => true,
		'show_in_rest'        => false,
	) );
}
add_action( 'init', 'tvbc_register_cpts' );
