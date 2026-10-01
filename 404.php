<?php get_header(); ?>
<section class="hero hero--page">
	<?php echo tvbc_pattern( 'hero__pattern' ); // phpcs:ignore ?>
	<div class="container hero__inner">
		<div class="hero__copy">
			<p class="eyebrow">404</p>
			<h1 class="hero__title"><?php echo esc_html( tvbc_ui( 'e404_title' ) ); ?></h1>
			<p class="hero__text"><?php echo esc_html( tvbc_ui( 'e404_text' ) ); ?></p>
			<div class="hero__actions"><a class="btn btn--main" href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php echo esc_html( tvbc_ui( 'e404_btn' ) ); ?></a></div>
		</div>
	</div>
</section>
<?php get_footer(); ?>
