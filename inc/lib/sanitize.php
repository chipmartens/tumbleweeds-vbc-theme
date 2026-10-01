<?php

/**
 * Sanitize WordPress header
 */
function head_cleanup() {
	remove_action('wp_head', 'rsd_link');
	remove_action('wp_head', 'wlwmanifest_link');
	remove_action('wp_head', 'adjacent_posts_rel_link_wp_head', 10, 0);
	remove_action('wp_head', 'wp_generator');
	remove_action('wp_head', 'wp_shortlink_wp_head', 10, 0);
	remove_action('wp_head', 'print_emoji_detection_script', 7);
	remove_action('admin_print_scripts', 'print_emoji_detection_script');
	remove_action('wp_print_styles', 'print_emoji_styles');
	remove_action('admin_print_styles', 'print_emoji_styles');
	remove_action('wp_head', 'wp_oembed_add_discovery_links');
	remove_action('wp_head', 'wp_oembed_add_host_js');
	remove_action('wp_head', 'rest_output_link_wp_head', 10, 0);
	add_filter('use_default_gallery_style', '__return_false');
}
add_action('init', 'head_cleanup');

// Clean up archive titles
add_filter( 'get_the_archive_title_prefix', '__return_false' );

// Comments are off: this is a club site, not a blog community.
function disable_comments() {
	remove_post_type_support('post', 'comments');
	remove_post_type_support('page', 'comments');
	add_filter('comments_open', '__return_false', 99);
	add_filter('pings_open', '__return_false', 99);
}
add_action('init', 'disable_comments');

?>
