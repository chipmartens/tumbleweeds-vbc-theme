<?php
/*
Theme Name: Tumbleweeds Volleyball Club
Object: Footer (footer.php)
Text Domain: tvbc
*/

// vars
$email          = tvbc_opt( 'contact_email' );
$socials        = tvbc_opt( 'socials' );
$location       = tvbc_opt( 'club_location' );
$contact_link   = tvbc_opt( 'footer_contact_link' );
$blurb          = tvbc_opt( 'footer_blurb' );
$signup_title   = tvbc_opt( 'footer_signup_title' );
$signup_code    = tvbc_opt( 'footer_signup_code' );
$status_line    = tvbc_opt( 'footer_status_line' );
$small_print    = tvbc_opt( 'footer_small_print' );
$helpline_name  = tvbc_opt( 'helpline_name' );
$helpline_phone = tvbc_opt( 'helpline_phone' );
$complaints     = tvbc_opt( 'complaints_contact' );
$logo_text      = tvbc_opt( 'logo_text' ) ?: 'Tumbleweeds';
?>

<footer class="site-footer">

	<?php echo str_replace( '<img', '<img aria-hidden="true"', tvbc_mark( true, 'footer__wreath', 560 ) ); // phpcs:ignore ?>

	<div class="container-2xl footer__container">

		<div class="footer__newsletter">
			<?php if ( $signup_title ) : ?>
			<h2 class="footer__heading"><?php echo esc_html( $signup_title ); ?></h2>
			<?php endif; ?>
			<?php if ( $signup_code ) : ?>
			<div class="newsletter__form"><?php echo $signup_code; // phpcs:ignore -- embed code pasted by an admin in Club settings ?></div>
			<?php elseif ( $email ) : ?>
			<!-- No sign-up form code in Club settings: opens the visitor's email app addressed to the club. -->
			<form class="newsletter__form" data-mailto-form data-mailto="<?php echo esc_attr( $email ); ?>" data-subject="Add me to club updates" action="mailto:<?php echo esc_attr( $email ); ?>" method="post" enctype="text/plain">
				<label for="signup-email" hidden><?php echo esc_html( tvbc_ui( 'email_ph' ) ); ?></label>
				<input id="signup-email" name="email" type="email" placeholder="<?php echo esc_attr( tvbc_ui( 'email_ph' ) ); ?>" required>
				<button class="btn btn--light" type="submit"><?php echo esc_html( tvbc_ui( 'sign_up' ) ); ?></button>
			</form>
			<?php endif; ?>
		</div>

		<div class="footer__columns">

			<div class="footer__column footer__brand">
				<a class="footer__logo" href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home"><?php echo tvbc_mark( true, '', 48 ); // phpcs:ignore ?><?php echo wp_kses( preg_replace( '/ /', '<br>', esc_html( get_bloginfo( 'name', 'display' ) ), 1 ), array( 'br' => array() ) ); ?></a>
				<?php if ( $blurb ) : ?>
				<p class="footer__blurb"><?php echo esc_html( $blurb ); ?></p>
				<?php endif; ?>
			</div>

			<div class="footer__column">
				<h3 class="footer__title"><?php esc_html_e( 'The club', 'tvbc' ); ?></h3>
				<?php wp_nav_menu( array(
					'theme_location' => 'footer-menu',
					'container'      => false,
					'menu_class'     => 'menu',
					'fallback_cb'    => false,
					'depth'          => 1,
				) ); ?>
			</div>

			<div class="footer__column">
				<h3 class="footer__title"><?php esc_html_e( 'Contact', 'tvbc' ); ?></h3>
				<ul class="menu">
					<?php if ( $email ) : ?><li><a href="mailto:<?php echo esc_attr( $email ); ?>"><?php echo esc_html( $email ); ?></a></li><?php endif; ?>
					<?php if ( is_array( $socials ) ) : foreach ( $socials as $s ) : if ( empty( $s['social_url'] ) ) { continue; } ?>
					<li><a href="<?php echo esc_url( $s['social_url'] ); ?>" target="_blank" rel="noopener"><?php echo esc_html( $s['social_label'] ?: ucfirst( $s['social_network'] ) ); ?></a></li>
					<?php endforeach; endif; ?>
					<?php if ( ! empty( $contact_link['url'] ) ) : ?><li><a href="<?php echo esc_url( $contact_link['url'] ); ?>"><?php echo esc_html( $contact_link['title'] ); ?></a></li><?php endif; ?>
					<?php if ( $location ) : ?><li><?php echo esc_html( $location ); ?></li><?php endif; ?>
				</ul>
			</div>

			<div class="footer__column">
				<h3 class="footer__title"><?php esc_html_e( 'If something goes wrong', 'tvbc' ); ?></h3>
				<ul class="menu">
					<?php if ( $helpline_name ) : ?><li><?php echo esc_html( $helpline_name ); ?></li><?php endif; ?>
					<?php if ( $helpline_phone ) : ?><li><a href="tel:<?php echo esc_attr( tvbc_tel( $helpline_phone ) ); ?>"><?php echo esc_html( $helpline_phone ); ?></a></li><?php endif; ?>
					<?php if ( $complaints ) : ?><li><?php echo esc_html( 'Club complaints contact: ' . $complaints ); ?></li><?php endif; ?>
				</ul>
			</div>

		</div>

		<div class="footer__copyright">
			<span class="copyright__text">&copy; <?php echo esc_html( gmdate( 'Y' ) ); ?> <?php echo esc_html( get_bloginfo( 'name', 'display' ) ); ?>. <?php echo esc_html( $status_line ); ?></span>
			<?php if ( $small_print ) : ?><span class="copyright__small"><?php echo esc_html( $small_print ); ?></span><?php endif; ?>
		</div>

	</div>

</footer>

<?php wp_footer(); ?>

</body>
</html>
