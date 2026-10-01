<?php

/**
 * Custom Query Args
 */
function my_max_post_queries( $query ) {
}
add_action( 'pre_get_posts', 'my_max_post_queries' );

/**
 * Coaches in the order the editor sets (the Order box), for the People section.
 */
function tvbc_coaches_query( $ids = array() ) {
	$args = array(
		'post_type'      => 'coach',
		'posts_per_page' => -1,
		'orderby'        => 'menu_order title',
		'order'          => 'ASC',
	);
	if ( $ids ) {
		$args['post__in'] = array_map( 'intval', $ids );
		$args['orderby']  = 'post__in';
	}
	return new WP_Query( $args );
}

/**
 * Latest news posts for the News section.
 */
function tvbc_news_query( $count = 12 ) {
	return new WP_Query( array(
		'post_type'           => 'post',
		'posts_per_page'      => max( 1, (int) $count ),
		'ignore_sticky_posts' => true,
		'orderby'             => 'date',
		'order'               => 'DESC',
	) );
}

?>
