<?php
/*
Object: Single news post
*/
get_header();
while ( have_posts() ) :
	the_post();
	?>
	<section class="hero hero--page">
		<?php echo tvbc_pattern( 'hero__pattern' ); // phpcs:ignore ?>
		<div class="container hero__inner">
			<div class="hero__copy">
				<p class="eyebrow"><?php echo esc_html( get_the_date( 'F j, Y' ) ); ?></p>
				<h1 class="hero__title hero__title--post"><?php echo tvbc_inline( get_the_title() ); // phpcs:ignore ?></h1>
			</div>
		</div>
	</section>
	<section class="section section--light">
		<div class="container">
			<article class="prose"><?php the_content(); ?></article>
			<p class="prose__back"><a class="btn btn--plain" href="<?php echo esc_url( get_permalink( get_option( 'page_for_posts' ) ) ); ?>"><?php echo esc_html( tvbc_ui( 'all_news' ) ); ?></a></p>
		</div>
	</section>
	<?php
endwhile;
get_footer();
