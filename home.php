<?php
/*
Object: Posts page (News). Hero and sections come from the page assigned as the posts page.
*/
get_header();
get_template_part( 'template-parts/content', 'hero' );
get_template_part( 'template-parts/content', 'flexcontent' );
get_footer();
