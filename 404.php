<?php
/*
Theme Name: Tumbleweeds Volleyball Club
Object: 404 (404.php)
Text Domain: tvbc
*/

get_header(); ?>

	<header class="hero hero--page hero--plain">
		<div class="hero__inner">
			<div class="container-2xl hero__container">
				<div class="hero__content">
					<span class="hero__tag"><span class="dot"></span><?php echo esc_html( tvbc_ui( 'e404_tag' ) ); ?></span>
					<h1 class="hero__title"><?php echo esc_html( tvbc_ui( 'e404_title' ) ); ?></h1>
					<p class="hero__lede"><?php echo esc_html( tvbc_ui( 'e404_text' ) ); ?></p>
					<div class="hero__ctas"><a class="btn btn--light" href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php echo esc_html( tvbc_ui( 'e404_btn' ) ); ?></a></div>
				</div>
			</div>
		</div>
	</header>

	<main id="main"></main>

<?php get_footer(); ?>
