<?php
/*
Theme Name: Tumbleweeds Volleyball Club
Object: Index (index.php). The posts page (News) uses the flexible content of the page assigned as the posts page.
Text Domain: tvbc
*/

get_header(); ?>

	<?php get_template_part('template-parts/content', 'hero'); ?>

	<main id="main">
		<?php get_template_part('template-parts/content', 'flexcontent');  ?>
	</main>

<?php get_footer(); ?>
