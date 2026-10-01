<?php
/*
Object: Header (header.php)
*/
$cta_label = tvbc_opt( 'header_cta_label' );
$cta_link  = function_exists( 'get_field' ) ? ( function_exists( 'acf_add_options_page' ) ? get_field( 'header_cta_link', 'option' ) : get_field( 'header_cta_link', (int) get_option( 'page_on_front' ) ) ) : null;
?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>">
	<meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1">
	<meta name="theme-color" content="#283B27">
	<link rel="icon" type="image/svg+xml" href="<?php echo esc_url( get_template_directory_uri() . '/assets/img/brand/tumbleweeds-mark-small.svg' ); ?>">
	<link rel="preload" href="<?php echo esc_url( get_template_directory_uri() . '/assets/fonts/barlow-condensed-800.woff2' ); ?>" as="font" type="font/woff2" crossorigin>
	<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<a class="skip-link" href="#main"><?php echo esc_html( tvbc_ui( 'skip' ) ); ?></a>

<header class="site-header">
	<div class="container site-header__inner">
		<a class="site-header__logo" href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home" aria-label="<?php echo esc_attr( get_bloginfo( 'name' ) ); ?>, home">
			<?php echo tvbc_logo( 'horizontal' ); // phpcs:ignore ?>
		</a>

		<nav class="site-header__nav" id="site-nav" aria-label="Primary">
			<?php
			wp_nav_menu( array(
				'theme_location' => 'primary',
				'container'      => false,
				'menu_class'     => 'menu',
				'fallback_cb'    => false,
				'depth'          => 1,
			) );
			?>
			<?php if ( $cta_label && tvbc_url( $cta_link ) ) : ?>
				<div class="site-header__cta-mobile"><?php echo tvbc_btn( $cta_label, $cta_link, 'main' ); // phpcs:ignore ?></div>
			<?php endif; ?>
		</nav>

		<?php if ( $cta_label && tvbc_url( $cta_link ) ) : ?>
			<div class="site-header__cta"><?php echo tvbc_btn( $cta_label, $cta_link, 'main' ); // phpcs:ignore ?></div>
		<?php endif; ?>

		<button class="site-header__toggle" type="button" aria-expanded="false" aria-controls="site-nav">
			<span class="site-header__toggle-label">Menu</span>
			<span class="site-header__toggle-bars" aria-hidden="true"></span>
		</button>
	</div>
</header>

<main id="main">
