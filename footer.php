<?php
/*
Object: Footer (footer.php)
*/
$email = tvbc_opt( 'contact_email' );
$ig    = tvbc_opt( 'instagram_handle' );
$igurl = tvbc_opt( 'instagram_url' );
$blurb = tvbc_opt( 'footer_blurb' );
?>
</main>

<footer class="site-footer">
	<div class="container">
		<div class="site-footer__grid">
			<div class="site-footer__brand">
				<?php echo tvbc_logo( 'stacked', true ); // phpcs:ignore ?>
				<?php if ( $blurb ) : ?>
					<p class="site-footer__blurb"><?php echo tvbc_inline( $blurb ); ?></p>
				<?php endif; ?>
			</div>

			<nav class="site-footer__col" aria-label="Footer">
				<h2 class="site-footer__title">The club</h2>
				<?php
				wp_nav_menu( array(
					'theme_location' => 'primary',
					'container'      => false,
					'menu_class'     => 'site-footer__list',
					'fallback_cb'    => false,
					'depth'          => 1,
				) );
				?>
			</nav>

			<div class="site-footer__col">
				<h2 class="site-footer__title">Contact</h2>
				<ul class="site-footer__list">
					<?php if ( $email ) : ?><li><a href="mailto:<?php echo esc_attr( $email ); ?>"><?php echo esc_html( $email ); ?></a></li><?php endif; ?>
					<?php if ( $ig ) : ?><li><a href="<?php echo esc_url( $igurl ); ?>" rel="noopener"><?php echo esc_html( $ig ); ?> on Instagram</a></li><?php endif; ?>
					<li>Kamloops, BC</li>
				</ul>
			</div>

			<div class="site-footer__col">
				<h2 class="site-footer__title">If something goes wrong</h2>
				<p class="site-footer__text"><?php echo esc_html( tvbc_opt( 'helpline_name' ) ); ?><br><a href="tel:<?php echo esc_attr( tvbc_tel( tvbc_opt( 'helpline_phone' ) ) ); ?>"><?php echo esc_html( tvbc_opt( 'helpline_phone' ) ); ?></a></p>
				<p class="site-footer__text">Club complaints contact: <?php echo tvbc_inline( tvbc_opt( 'complaints_contact' ) ); ?></p>
			</div>
		</div>

		<div class="site-footer__base">
			<p>&copy; <?php echo esc_html( gmdate( 'Y' ) ); ?> Tumbleweeds Volleyball Club. A Volleyball BC member club, Zone 2 Thompson-Okanagan.</p>
		</div>
	</div>
</footer>

<?php wp_footer(); ?>
</body>
</html>
