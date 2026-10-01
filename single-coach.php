<?php
/*
Object: Single coach
*/
get_header();
while ( have_posts() ) :
	the_post();
	$role  = get_field( 'role' );
	$teams = get_field( 'teams' );
	$photo = get_field( 'photo' );
	$bio   = get_field( 'bio', false, false );
	$creds = get_field( 'credentials' );
	?>
	<section class="hero hero--page">
		<?php echo tvbc_pattern( 'hero__pattern' ); // phpcs:ignore ?>
		<div class="container hero__inner">
			<div class="hero__copy">
				<p class="eyebrow"><?php echo tvbc_inline( $role ); ?></p>
				<h1 class="hero__title"><?php echo tvbc_inline( get_the_title() ); // phpcs:ignore ?></h1>
				<?php if ( $teams ) : ?><p class="hero__text"><?php echo tvbc_inline( $teams ); ?></p><?php endif; ?>
			</div>
		</div>
	</section>
	<section class="section section--light">
		<div class="container bio">
			<div class="bio__photo">
				<?php echo tvbc_pattern( 'bio__pattern' ); // phpcs:ignore ?>
				<?php echo tvbc_img( $photo, 'bio__img', 'large' ); // phpcs:ignore ?>
			</div>
			<div class="bio__body">
				<?php if ( $bio ) : ?><div class="prose"><?php echo wp_kses_post( wpautop( $bio ) ); ?></div><?php endif; ?>
				<?php if ( $creds ) : ?>
					<ul class="ticks">
						<?php foreach ( $creds as $c ) : ?><li><?php echo tvbc_inline( $c['line'] ); ?></li><?php endforeach; ?>
					</ul>
				<?php endif; ?>
				<p><a class="btn btn--plain" href="<?php echo esc_url( home_url( '/our-coaches/' ) ); ?>">All coaches</a></p>
			</div>
		</div>
	</section>
	<?php
endwhile;
get_footer();
