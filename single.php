<?php
/*
Theme Name: Tumbleweeds Volleyball Club
Object: Single news post (single.php)
Text Domain: tvbc
*/

get_header(); ?>

	<?php get_template_part('template-parts/content', 'hero'); ?>

	<main id="main">

	<?php while ( have_posts() ) : the_post();
		$post_id   = get_the_ID();
		$all       = tvbc_news_query( 50 );
		$ids       = wp_list_pluck( $all->posts, 'ID' );
		$pos       = array_search( $post_id, $ids, true );
		$next_id   = $ids ? $ids[ ( (int) $pos + 1 ) % count( $ids ) ] : 0;
		$list_url  = get_permalink( get_option( 'page_for_posts' ) ) ?: home_url( '/' );
	?>

		<section class="article-section surface">

			<div class="container-2xl article">

				<div class="article__meta fade-up">
					<span class="article__date"><?php echo esc_html( get_the_date( 'M j, Y' ) ); ?></span>
					<p class="section__eyebrow"><b><?php echo esc_html( numbered_sections() ); ?></b><?php esc_html_e( 'News', 'tvbc' ); ?></p>
					<a class="link" href="<?php echo esc_url( $list_url ); ?>"><?php echo esc_html( tvbc_ui( 'all_news' ) ); ?> <?php echo tvbc_icon( 'arrow' ); // phpcs:ignore ?></a>
				</div>

				<div class="article__content content fade-up">
					<?php the_content(); ?>
				</div>

			</div>

		</section>

		<section class="pager-section surface">
			<div class="container-2xl">
				<div class="pager fade-up">
					<a class="pager__link" href="<?php echo esc_url( $list_url ); ?>"><span><span class="pager__label"><?php esc_html_e( 'News', 'tvbc' ); ?></span><strong class="pager__title"><?php echo esc_html( tvbc_ui( 'all_news' ) ); ?></strong></span><?php echo tvbc_icon( 'arrow' ); // phpcs:ignore ?></a>
					<?php if ( $next_id && $next_id !== $post_id ) : ?>
					<a class="pager__link" href="<?php echo esc_url( get_permalink( $next_id ) ); ?>"><span><span class="pager__label"><?php echo esc_html( tvbc_ui( 'next' ) ); ?></span><strong class="pager__title"><?php echo esc_html( get_the_title( $next_id ) ); ?></strong></span><?php echo tvbc_icon( 'arrow' ); // phpcs:ignore ?></a>
					<?php endif; ?>
				</div>
			</div>
		</section>

		<?php
		tvbc_band(
			get_field( 'band_image', $post_id ),
			get_field( 'band_heading', $post_id ),
			get_field( 'band_heading_accent', $post_id ),
			get_field( 'band_button_1', $post_id ),
			get_field( 'band_button_2', $post_id )
		);
		?>

	<?php endwhile; ?>

	</main>

<?php get_footer(); ?>
