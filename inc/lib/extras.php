<?php
// Small template helpers: logo, nav, dates.

/** The club logo. Uses the finished SVG lockups in assets/img/brand/. $reverse = for dark backgrounds. */
function tvbc_logo( $layout = 'horizontal', $reverse = false ) {
	$file = 'tumbleweeds-lockup-' . $layout . ( $reverse ? '-reverse' : '' ) . '.svg';
	$uri  = get_template_directory_uri() . '/assets/img/brand/' . $file;
	return '<img class="logo logo--' . esc_attr( $layout ) . '" src="' . esc_url( $uri ) . '" alt="' . esc_attr( get_bloginfo( 'name' ) ) . '" width="' . ( 'horizontal' === $layout ? 340 : 200 ) . '" height="' . ( 'horizontal' === $layout ? 104 : 190 ) . '">';
}

/** Cut-out placeholder image shipped with the theme (used when a coach has no photo). */
function tvbc_theme_img( $path ) {
	return get_template_directory_uri() . '/assets/img/' . ltrim( $path, '/' );
}

/** Body class for the hero style, so the header can adapt. */
add_filter( 'body_class', function ( $classes ) {
	if ( function_exists( 'get_field' ) && is_page() ) {
		$classes[] = 'hero-' . ( get_field( 'hero_style' ) ?: 'page' );
	}
	return $classes;
} );

/** Document title: "Page | Tumbleweeds Volleyball Club". */
add_filter( 'document_title_separator', function () {
	return '|';
} );

/** Meta description from the hero intro, so every page has one without extra work. */
add_action( 'wp_head', function () {
	if ( ! is_page() || ! function_exists( 'get_field' ) ) {
		return;
	}
	$d = get_field( 'hero_text' );
	if ( $d ) {
		echo '<meta name="description" content="' . esc_attr( wp_strip_all_tags( $d ) ) . '">' . "\n";
	}
} );
