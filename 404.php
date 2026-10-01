<?php get_header(); ?>
<section class="hero hero--page">
	<?php echo tvbc_pattern( 'hero__pattern' ); // phpcs:ignore ?>
	<div class="container hero__inner">
		<div class="hero__copy">
			<p class="eyebrow">404</p>
			<h1 class="hero__title">That page is not here.</h1>
			<p class="hero__text">Try the menu above, or head back to the home page.</p>
			<div class="hero__actions"><a class="btn btn--main" href="<?php echo esc_url( home_url( '/' ) ); ?>">Back home</a></div>
		</div>
	</div>
</section>
<?php get_footer(); ?>
