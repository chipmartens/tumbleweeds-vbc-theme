<?php
// Custom post types: coach (live) and team (rosters later).

add_action( 'init', function () {
	register_post_type( 'coach', array(
		'labels'        => array( 'name' => 'Coaches', 'singular_name' => 'Coach', 'add_new_item' => 'Add coach', 'edit_item' => 'Edit coach', 'all_items' => 'All coaches' ),
		'public'        => true,
		'has_archive'   => false,
		'menu_icon'     => 'dashicons-groups',
		'menu_position' => 21,
		'supports'      => array( 'title', 'page-attributes' ), // page-attributes = the Order box
		'rewrite'       => array( 'slug' => 'coaches', 'with_front' => false ),
	) );
	register_post_type( 'team', array(
		'labels'             => array( 'name' => 'Teams', 'singular_name' => 'Team', 'add_new_item' => 'Add team', 'edit_item' => 'Edit team', 'all_items' => 'All teams' ),
		'public'             => false,
		'publicly_queryable' => false,
		'show_ui'            => true,
		'menu_icon'          => 'dashicons-flag',
		'menu_position'      => 22,
		'supports'           => array( 'title', 'page-attributes' ),
	) );
} );
