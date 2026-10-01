<?php
/*
Theme Name: Tumbleweeds Volleyball Club
Object: Single coach (single-coach.php)
Text Domain: tvbc
*/

get_header(); ?>

	<?php get_template_part('template-parts/content', 'hero'); ?>

	<main id="main">

	<?php while ( have_posts() ) : the_post();
		$coach_id    = get_the_ID();
		$role        = get_field( 'coach_role', $coach_id );
		$photo       = get_field( 'coach_photo', $coach_id );
		$bio         = get_field( 'coach_bio', $coach_id );
		$facts       = get_field( 'coach_facts', $coach_id );
		$coaches     = tvbc_coaches_query();
		$ids         = wp_list_pluck( $coaches->posts, 'ID' );
		$pos         = array_search( $coach_id, $ids, true );
		$next_id     = $ids ? $ids[ ( (int) $pos + 1 ) % count( $ids ) ] : 0;
		$list_page   = tvbc_opt( 'coaches_page' );
		$list_url    = $list_page ? get_permalink( is_object( $list_page ) ? $list_page->ID : $list_page ) : home_url( '/' );
	?>

		<section class="bio surface last-module">

			<div class="container-2xl bio__inner">

				<div class="bio__media fade-up">
					<?php section_image( 'sheet', $photo, 'bio__image', false, true, null, false, get_the_title() ); ?>
				</div>

				<div class="bio__body fade-up">
					<p class="section__eyebrow"><b><?php echo esc_html( numbered_sections() ); ?></b><?php echo esc_html( $role ); ?></p>
					<h2 class="section__heading"><?php the_title(); ?></h2>
					<span class="bio__role"><?php echo esc_html( $role . ', ' . get_bloginfo( 'name', 'display' ) ); ?></span>
					<?php if ( $bio ) : ?><div class="content bio__content"><?php echo $bio; // phpcs:ignore ?></div><?php endif; ?>
					<?php
					// Facts reuse the section fact rows: label, answer, status tag
					$rows = array();
					if ( is_array( $facts ) ) {
						foreach ( $facts as $f ) {
							$rows[] = array( 'fact_label' => $f['fact_label'], 'fact_value' => $f['fact_value'], 'fact_tag' => $f['fact_tag'] );
						}
					}
					tvbc_facts( $rows );
					?>
				</div>

			</div>

		</section>

		<section class="pager-section surface">
			<div class="container-2xl">
				<div class="pager fade-up">
					<a class="pager__link" href="<?php echo esc_url( $list_url ); ?>"><span><span class="pager__label"><?php echo esc_html( tvbc_label( 'label_club', 'The club' ) ); ?></span><strong class="pager__title"><?php echo esc_html( tvbc_ui( 'all_coaches' ) ); ?></strong></span><?php echo tvbc_icon( 'arrow' ); // phpcs:ignore ?></a>
					<?php if ( $next_id && $next_id !== $coach_id ) : ?>
					<a class="pager__link" href="<?php echo esc_url( get_permalink( $next_id ) ); ?>"><span><span class="pager__label"><?php echo esc_html( tvbc_ui( 'next' ) ); ?></span><strong class="pager__title"><?php echo esc_html( get_the_title( $next_id ) ); ?></strong></span><?php echo tvbc_icon( 'arrow' ); // phpcs:ignore ?></a>
					<?php endif; ?>
				</div>
			</div>
		</section>

		<?php
		tvbc_band(
			get_field( 'band_image', $coach_id ),
			get_field( 'band_heading', $coach_id ),
			get_field( 'band_heading_accent', $coach_id ),
			get_field( 'band_button_1', $coach_id ),
			get_field( 'band_button_2', $coach_id )
		);
		?>

	<?php endwhile; ?>

	</main>

<?php get_footer(); ?>
