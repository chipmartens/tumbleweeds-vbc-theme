<?php
/*
Theme Name: Tumbleweeds Volleyball Club
Object: Header (header.php)
Text Domain: tvbc
*/
$ann       = tvbc_announcement();
$cta_link  = tvbc_or_registration( tvbc_opt( 'header_cta' ), tvbc_opt( 'header_register' ) );
$logo_text = tvbc_opt( 'logo_text' ) ?: 'Tumbleweeds';
$extra     = tvbc_opt( 'phone_menu_link' );
$extra_li  = ( ! empty( $extra['url'] ) ) ? '<li class="menu-item menu-item--extra"><a href="' . esc_url( $extra['url'] ) . '">' . esc_html( $extra['title'] ) . '</a></li>' : '';
?>
<!DOCTYPE html>
<html class="no-js" <?php language_attributes(); ?>>

<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>" />
	<meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1" />

	<!-- Icons -->
	<?php tvbc_favicon(); ?>
	<meta name="theme-color" content="#172111">

	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
	<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Figtree:wght@300;400;500;600&family=Instrument+Serif:ital@1&display=swap" rel="stylesheet" />

	<script>
		document.documentElement.className = document.documentElement.className.replace("no-js", "js");
	</script>
<?php wp_enqueue_script( 'jquery' ); ?>
<?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
	<?php wp_body_open(); ?>
	<a class="skip-link" href="#main"><?php echo esc_html( tvbc_ui( 'skip' ) ); ?></a>

	<?php if ( $ann ) : ?>
	<div class="announcement">
		<?php echo esc_html( $ann['text'] ); ?>
		<?php if ( ! empty( $ann['link']['url'] ) ) : ?>
		<a href="<?php echo esc_url( $ann['link']['url'] ); ?>"><?php echo esc_html( $ann['link']['title'] ); ?></a>
		<?php endif; ?>
	</div>
	<?php endif; ?>

	<header class="site-header">

		<div class="container-2xl">

			<div class="site-logo">
				<a href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home" aria-label="<?php echo esc_attr( get_bloginfo( 'name', 'display' ) ); ?>, home"><?php echo tvbc_mark( false, '', 40 ); // phpcs:ignore ?><span><?php echo esc_html( $logo_text ); ?></span></a>
			</div>

			<nav class="site-nav" aria-label="<?php esc_attr_e( 'Main', 'tvbc' ); ?>">
				<?php
				wp_nav_menu( array(
					'theme_location' => 'header-menu',
					'container'      => false,
					'menu_class'     => 'menu',
					'menu_id'        => 'menu-header',
					'fallback_cb'    => 'header_menu_cb',
					'depth'          => 1,
				) );
				?>
			</nav>

			<?php if ( ! empty( $cta_link['url'] ) ) : ?>
			<div class="site-cta"><?php echo tvbc_btn( $cta_link, 'btn--sun btn--sm' ); // phpcs:ignore ?></div>
			<?php endif; ?>

			<button class="menu-toggle" type="button" aria-label="<?php echo esc_attr( tvbc_ui( 'menu_open' ) ); ?>" aria-expanded="false" aria-controls="drawer"><?php echo tvbc_icon( 'menu' ); // phpcs:ignore ?></button>

		</div>

	</header>

	<div class="drawer" id="drawer" aria-hidden="true">
		<div class="drawer__top">
			<span class="site-logo"><?php echo tvbc_mark( true, '', 40 ); // phpcs:ignore ?><span><?php echo esc_html( $logo_text ); ?></span></span>
			<button class="menu-toggle menu-toggle--close" type="button" aria-label="<?php echo esc_attr( tvbc_ui( 'menu_close' ) ); ?>" data-menu-close><?php echo tvbc_icon( 'close' ); // phpcs:ignore ?></button>
		</div>
		<nav class="drawer__nav" aria-label="<?php esc_attr_e( 'Mobile', 'tvbc' ); ?>">
			<?php
			wp_nav_menu( array(
				'theme_location' => 'header-menu',
				'container'      => false,
				'menu_class'     => 'menu',
				'menu_id'        => 'menu-drawer',
				'items_wrap'     => '<ul id="%1$s" class="%2$s">%3$s' . str_replace( '%', '%%', $extra_li ) . '</ul>',
				'fallback_cb'    => false,
				'depth'          => 1,
			) );
			?>
		</nav>
		<?php if ( ! empty( $cta_link['url'] ) ) : ?>
		<?php echo tvbc_btn( $cta_link, 'btn--sun' ); // phpcs:ignore ?>
		<?php endif; ?>
	</div>
