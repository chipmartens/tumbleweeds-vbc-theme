<?php
/*
Object: Page (page.php). Hero and sections come from fields.
*/
get_header();
while ( have_posts() ) :
	the_post();
	get_template_part( 'template-parts/content', 'hero' );
	get_template_part( 'template-parts/content', 'flexcontent' );
endwhile;
get_footer();
