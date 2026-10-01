<?php

/**
 * Search, sharing, icons and analytics.
 * Yoast SEO (free, installed through TGMPA) owns titles, descriptions and Open Graph when it is active.
 * Without it the theme prints a small fallback so a shared link still gets a title, text and picture.
 */

function tvbc_yoast_active() {
	return defined( 'WPSEO_VERSION' );
}

// Browser tab icons: the one set in Club settings, else the Site Icon from the Customizer, else the club mark set
function tvbc_favicon() {
	$fav = function_exists( 'tvbc_opt' ) ? tvbc_opt( 'favicon' ) : '';
	if ( ! empty( $fav['url'] ) ) {
		echo '<link rel="icon" href="' . esc_url( $fav['url'] ) . '">' . "\n";
	} elseif ( ! has_site_icon() ) {
		echo '<link rel="icon" type="image/svg+xml" href="' . esc_url( tvbc_theme_img( 'tumbleweeds-official-mark.svg' ) ) . '">' . "\n";
		echo '<link rel="icon" type="image/png" sizes="32x32" href="' . esc_url( tvbc_theme_img( 'favicon-32.png' ) ) . '">' . "\n";
		echo '<link rel="icon" type="image/png" sizes="192x192" href="' . esc_url( tvbc_theme_img( 'icon-192.png' ) ) . '">' . "\n";
		echo '<link rel="icon" type="image/png" sizes="512x512" href="' . esc_url( tvbc_theme_img( 'icon-512.png' ) ) . '">' . "\n";
		echo '<link rel="apple-touch-icon" sizes="180x180" href="' . esc_url( tvbc_theme_img( 'apple-touch-icon.png' ) ) . '">' . "\n";
	}
}

// Short description of the current page: what the editor already wrote (hero text, coach summary, post excerpt)
function tvbc_page_description() {
	$id = tvbc_context_id();
	$d  = '';
	if ( function_exists( 'get_field' ) ) {
		if ( is_singular( 'coach' ) ) {
			$d = get_field( 'coach_summary', $id );
		} elseif ( is_singular( 'post' ) ) {
			$d = get_the_excerpt( $id );
		} elseif ( $id ) {
			$d = get_field( 'hero_subhead', $id );
		}
	}
	return wp_strip_all_tags( $d ? $d : get_bloginfo( 'description' ) );
}

// The default sharing picture: Club settings, else the 1200 by 630 picture that ships with the theme
function tvbc_social_image() {
	$img = function_exists( 'tvbc_opt' ) ? tvbc_opt( 'social_image' ) : '';
	if ( ! empty( $img['url'] ) ) {
		return $img['url'];
	}
	return tvbc_theme_img( 'tumbleweeds-social.jpg' );
}

// Meta description and Open Graph, only when Yoast SEO is not active
add_action( 'wp_head', 'tvbc_meta_fallback', 5 );
function tvbc_meta_fallback() {
	if ( tvbc_yoast_active() ) {
		return;
	}
	$desc  = tvbc_page_description();
	$title = wp_get_document_title();
	$url   = is_singular() ? get_permalink() : home_url( '/' );
	$image = tvbc_social_image();
	if ( is_singular( 'post' ) && has_post_thumbnail() ) {
		$image = get_the_post_thumbnail_url( null, 'hero' );
	}
	if ( $desc ) {
		echo '<meta name="description" content="' . esc_attr( $desc ) . '">' . "\n";
	}
	echo '<meta property="og:type" content="' . ( is_singular( 'post' ) ? 'article' : 'website' ) . '">' . "\n";
	echo '<meta property="og:site_name" content="' . esc_attr( get_bloginfo( 'name', 'display' ) ) . '">' . "\n";
	echo '<meta property="og:title" content="' . esc_attr( $title ) . '">' . "\n";
	if ( $desc ) {
		echo '<meta property="og:description" content="' . esc_attr( $desc ) . '">' . "\n";
	}
	echo '<meta property="og:url" content="' . esc_url( $url ) . '">' . "\n";
	echo '<meta property="og:image" content="' . esc_url( $image ) . '">' . "\n";
	echo '<meta name="twitter:card" content="summary_large_image">' . "\n";
}

/**
 * Google Analytics 4. Nothing is printed unless Club settings holds a measurement ID.
 * Default is cookie-free: consent mode starts at denied, so GA counts visits without setting cookies.
 * People who can edit the site are not counted.
 */
add_action( 'wp_head', 'tvbc_analytics', 20 );
function tvbc_analytics() {
	$id = trim( (string) tvbc_opt( 'ga4_id' ) );
	if ( ! preg_match( '/^G-[A-Z0-9]{4,}$/', $id ) || current_user_can( 'edit_posts' ) ) {
		return;
	}
	$storage = tvbc_opt( 'ga4_cookies' ) ? 'granted' : 'denied';
	?>
<script async src="https://www.googletagmanager.com/gtag/js?id=<?php echo esc_attr( $id ); ?>"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('consent', 'default', { analytics_storage: '<?php echo esc_js( $storage ); ?>', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' });
gtag('js', new Date());
gtag('config', '<?php echo esc_js( $id ); ?>', { allow_google_signals: false, allow_ad_personalization_signals: false });
</script>
<?php
}
