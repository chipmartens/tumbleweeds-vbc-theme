<?php
// Hero: fields are Top of page on each Page. The posts page (News) reads the page it is assigned to.
$hero_id = is_home() ? (int) get_option( 'page_for_posts' ) : get_the_ID();
if ( ! function_exists( 'get_field' ) || ! $hero_id ) {
	return;
}
$style   = get_field( 'hero_style', $hero_id ) ?: 'page';
$eyebrow = get_field( 'hero_eyebrow', $hero_id );
$heading = get_field( 'hero_heading', $hero_id ) ?: get_the_title( $hero_id );
$text    = get_field( 'hero_text', $hero_id );
$buttons = get_field( 'hero_buttons', $hero_id );
$note    = get_field( 'hero_note', $hero_id );
if ( tvbc_dead( $note ) ) {
	$note = '';
}
$photo   = ( 'home' === $style ) ? get_field( 'hero_photo', $hero_id ) : false;
?>
<section class="hero hero--<?php echo esc_attr( $style ); ?>">
	<?php echo tvbc_pattern( 'hero__pattern' ); // phpcs:ignore ?>
	<div class="container hero__inner">
		<div class="hero__copy">
			<?php if ( $eyebrow ) : ?><p class="eyebrow"><?php echo tvbc_inline( $eyebrow ); ?></p><?php endif; ?>
			<h1 class="hero__title"><?php echo tvbc_inline( $heading ); ?></h1>
			<?php if ( $text ) : ?><p class="hero__text"><?php echo tvbc_inline( $text ); ?></p><?php endif; ?>
			<?php if ( $buttons ) : ?>
				<div class="hero__actions">
					<?php
					foreach ( $buttons as $n => $b ) {
						$s = ( 'home' === $style ) ? ( 0 === $n ? 'sun' : 'line' ) : ( 0 === $n ? 'main' : 'plain' );
						echo tvbc_btn( $b['label'], $b['link'], $s ); // phpcs:ignore
					}
					?>
				</div>
			<?php endif; ?>
			<?php if ( $note ) : ?><p class="hero__note"><?php echo tvbc_inline( $note ); ?></p><?php endif; ?>
		</div>
		<?php if ( $photo ) : ?>
			<div class="hero__photo"><?php echo tvbc_img( $photo, 'hero__img', 'large' ); // phpcs:ignore ?></div>
		<?php endif; ?>
	</div>
</section>
