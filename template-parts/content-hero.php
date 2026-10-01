<?php

// Resolve what the hero shows: a coach, a news post, or the fields on the page itself
// (the News page is the posts page, so it reads its own fields too).
$post_id = tvbc_context_id();

$hero_layout  = 'page';
$hero_image   = null;
$hero_x       = 50;
$hero_y       = 50;
$hero_tag     = '';
$hero_heading = '';
$hero_accent  = '';
$hero_subhead = '';
$hero_btn_1   = null;
$hero_btn_2   = null;
$hero_phone   = null;

if ( is_singular( 'coach' ) ) :
	$coach_role   = get_field( 'coach_role', $post_id );
	$hero_image   = get_field( 'coach_hero_image', $post_id );
	$hero_x       = get_field( 'hero_focus_x', $post_id );
	$hero_y       = get_field( 'hero_focus_y', $post_id );
	$hero_tag     = 'Our coaches';
	$hero_heading = get_the_title( $post_id );
	$hero_subhead = $coach_role ? $coach_role . ', ' . get_bloginfo( 'name', 'display' ) . '.' : '';
elseif ( is_singular( 'post' ) ) :
	$hero_image   = featured_image_obj( 0, $post_id );
	$hero_x       = get_field( 'hero_focus_x', $post_id );
	$hero_y       = get_field( 'hero_focus_y', $post_id );
	$hero_tag     = 'News, ' . get_the_date( 'M j, Y', $post_id );
	$hero_heading = get_the_title( $post_id );
else :
	if ( function_exists( 'get_field' ) && $post_id ) {
		$hero_layout = get_field( 'hero_layout', $post_id ) ?: 'page';
		$hero_image  = get_field( 'hero_image', $post_id );
		$hero_x      = get_field( 'hero_focus_x', $post_id );
		$hero_y      = get_field( 'hero_focus_y', $post_id );
		$hero_tag    = get_field( 'hero_tag', $post_id );
		$hero_heading = get_field( 'hero_heading', $post_id );
		$hero_accent = get_field( 'hero_heading_accent', $post_id );
		$hero_subhead = get_field( 'hero_subhead', $post_id );
		$hero_btn_1  = tvbc_or_registration( get_field( 'hero_button_1', $post_id ), get_field( 'hero_register', $post_id ) );
		$hero_btn_2  = get_field( 'hero_button_2', $post_id );
		$hero_phone  = get_field( 'hero_phone_focus', $post_id ) ? array( get_field( 'hero_phone_x', $post_id ), get_field( 'hero_phone_y', $post_id ) ) : null;
	}
	if ( ! $hero_heading ) {
		$hero_heading = get_the_title( $post_id );
	}
endif;

if ( 'none' === $hero_layout ) {
	return;
}

$is_home = ( 'home' === $hero_layout );
$badge   = $is_home ? tvbc_opt( 'badge_text' ) : '';
?>

<header class="hero hero--<?php echo $is_home ? 'home' : 'page'; ?><?php echo $hero_image ? '' : ' hero--plain'; ?>">

	<?php if ( $hero_image ) : ?>
		<?php section_image( 'hero', $hero_image, 'hero__image', false, true, null, true, null, tvbc_focus( $hero_x, $hero_y, $hero_phone ) ); ?>
	<?php endif; ?>

	<div class="hero__inner">

		<div class="container-2xl hero__container">

			<div class="hero__content">

				<?php if ( $hero_tag ) : ?>
				<span class="hero__tag"><span class="dot"></span><?php echo esc_html( $hero_tag ); ?></span>
				<?php endif; ?>

				<h1 class="hero__title"><?php echo tvbc_heading( $hero_heading, $hero_accent ); // phpcs:ignore ?></h1>

				<?php if ( $hero_subhead ) : ?>
				<p class="hero__lede"><?php echo esc_html( $hero_subhead ); ?></p>
				<?php endif; ?>

				<?php if ( ! empty( $hero_btn_1['url'] ) || ! empty( $hero_btn_2['url'] ) ) : ?>
				<div class="hero__ctas">
					<?php echo tvbc_btn( $hero_btn_1, 'btn--light', true ); // phpcs:ignore ?>
					<?php echo tvbc_btn( $hero_btn_2, 'btn--ghost' ); // phpcs:ignore ?>
				</div>
				<?php endif; ?>

			</div>

			<?php if ( $badge ) : ?>
			<div class="hero__badge" aria-hidden="true">
				<svg class="hero__ring" viewBox="0 0 184 184"><defs><path id="badge-circle" d="M92,92 m-76,0 a76,76 0 1,1 152,0 a76,76 0 1,1 -152,0"/></defs><text><textPath href="#badge-circle" textLength="472" lengthAdjust="spacing"><?php echo esc_html( $badge ); ?></textPath></text></svg>
				<?php echo tvbc_mark( false, '', 96 ); // phpcs:ignore ?>
			</div>
			<?php endif; ?>

		</div>

	</div>

</header>
