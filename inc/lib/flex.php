<?php

/**
 * Section helpers for template-parts/content-flexcontent.php.
 * They echo classes and markup from the current ACF sub row (get_sub_field) unless noted.
 */

// Little utility function - using to detect last row of the repeater, add special class to it
function is_last_row( $i, $total_rows ) {
	if ( $i == $total_rows ) {
		echo ' last-module';
	}
}

// Does the page end in a closing banner? (drives the footer overlap in CSS)
function tvbc_has_closing_band() {
	if ( is_singular( array( 'coach', 'post' ) ) ) {
		return (bool) get_field( 'band_image', get_queried_object_id() );
	}
	$id = tvbc_context_id();
	if ( ! $id || ! function_exists( 'get_field' ) ) {
		return false;
	}
	$rows = get_field( 'flex_content', $id );
	return is_array( $rows ) && $rows && 'section_band' === end( $rows )['acf_fc_layout'];
}

// Attach an ID to each section for #links: the editor's "link name" if set, else the heading, else section-N
function section_id( $id = null, $content = null, $echo = true ) {
	$anchor = sanitize_title( (string) get_sub_field( 'section_anchor' ) );
	if ( $anchor ) {
		$section_id = $anchor;
	} else {
		$content = $content ? $content : get_sub_field( 'section_heading' );
		if ( $content ) {
			$heading = strtolower( strip_tags( $content ) );
			$heading = str_replace( array( ' / ', ' - ', ' ', '&' ), array( '-', '-', '-', 'and' ), $heading );
			$heading = preg_replace( '/[^a-z0-9-]/', '', $heading );
			$section_id = 'section-' . trim( $heading, '-' );
		} else {
			$section_id = 'section-' . (int) $id;
		}
	}
	if ( $echo ) {
		echo esc_attr( $section_id );
	} else {
		return $section_id;
	}
}

// Function to get value of 'Section Background Color' (white paper is the default)
function section_bg_color() {
	$v = get_sub_field( 'section_bg_color' );
	if ( $v && in_array( $v, array( 'sage', 'sun', 'sand' ), true ) ) {
		echo ' surface--' . esc_attr( $v );
	}
}

// Numbered sections function: the next 01, 02, 03 on this page, for sections that ask for it
$numbered_sections = 0;
function numbered_sections() {
	global $numbered_sections;
	$numbered_sections++;
	return sprintf( '%02d', $numbered_sections );
}

// Render the section meta block: eyebrow (with auto number), heading (with italic accent), optional lede.
//
// Supported keys in $args:
//   container_class (string)  Extra class(es) on the .meta wrapper.
//   head_tag        (string)  Heading tag. Default 'h2'.
//   head_class      (string)  Heading class. Default 'section__heading'.
//   lede            (bool)    Also print the intro text under the heading (split layouts).
function section_meta( $args = array() ) {
	$args = wp_parse_args( $args, array(
		'container_class' => '',
		'head_tag'        => 'h2',
		'head_class'      => 'section__heading',
		'lede'            => false,
	) );

	$eyebrow = get_sub_field( 'section_eyebrow' );
	$heading = get_sub_field( 'section_heading' );
	$accent  = get_sub_field( 'section_heading_accent' );
	$lede    = $args['lede'] ? get_sub_field( 'section_lede' ) : '';
	$number  = get_sub_field( 'show_number' ) ? numbered_sections() : '';

	if ( ! $eyebrow && ! $heading && ! $lede ) {
		return;
	}

	echo '<div class="' . esc_attr( trim( 'meta ' . $args['container_class'] ) ) . '">';
	if ( $eyebrow || $number ) {
		echo '<p class="section__eyebrow">' . ( $number ? '<b>' . esc_html( $number ) . '</b>' : '' ) . esc_html( $eyebrow ) . '</p>';
	}
	if ( $heading ) {
		echo '<' . $args['head_tag'] . ' class="' . esc_attr( $args['head_class'] ) . '">' . tvbc_heading( $heading, $accent ) . '</' . $args['head_tag'] . '>';
	}
	if ( $lede ) {
		echo '<p class="section__subhead">' . esc_html( $lede ) . '</p>';
	}
	echo '</div>';
}

// Section head: the meta block, plus an optional short text or link on the right
function section_head( $args = array() ) {
	if ( ! get_sub_field( 'section_eyebrow' ) && ! get_sub_field( 'section_heading' ) && ! get_sub_field( 'show_number' ) ) {
		return; // nothing to show: no empty gap above the content
	}
	$side      = get_sub_field( 'section_side' );
	$side_html = '';
	if ( 'text' === $side && get_sub_field( 'section_side_text' ) ) {
		$side_html = '<p class="section__subhead section__subhead--side">' . esc_html( get_sub_field( 'section_side_text' ) ) . '</p>';
	} elseif ( 'link' === $side ) {
		$side_html = tvbc_link( get_sub_field( 'section_side_link' ) );
	}
	echo '<div class="surface__head fade-up">';
	section_meta( $args );
	echo $side_html;
	echo '</div>';
}

// Get 'Section Text' and output if not empty
function section_text( $pre = null, $post = null, $field = 'section_text' ) {
	$text = get_sub_field( $field );
	if ( $text ) {
		echo $pre . $text . $post;
	}
}

// Get 'Section CTA' link and output as a button
function section_cta( $classes = 'btn--dark', $field = 'section_cta', $arrow = false ) {
	$link = get_sub_field( $field );
	if ( 'section_cta' === $field ) {
		$link = tvbc_or_registration( $link, get_sub_field( 'cta_use_registration' ) );
	}
	echo tvbc_btn( $link, $classes . ' fade-up', $arrow );
}

// Fact rows: label, answer, small note, status tag. $rows = array of [fact_label, fact_value, fact_note, fact_tag]
function tvbc_facts( $rows, $class = '' ) {
	if ( empty( $rows ) || ! is_array( $rows ) ) {
		return;
	}
	echo '<div class="fact-list' . ( $class ? ' ' . esc_attr( $class ) : '' ) . '">';
	foreach ( $rows as $r ) {
		$value = ! empty( $r['fact_link']['url'] )
			? '<a class="link" href="' . esc_url( $r['fact_link']['url'] ) . '">' . esc_html( $r['fact_link']['title'] ) . '</a>'
			: ( isset( $r['fact_value'] ) ? tvbc_text( $r['fact_value'] ) : '' );
		$note  = ! empty( $r['fact_note'] ) ? '<small>' . esc_html( $r['fact_note'] ) . '</small>' : '';
		$tag   = ! empty( $r['fact_tag'] ) ? tvbc_tag( $r['fact_tag'] ) : '<span></span>';
		echo '<div class="fact"><span class="fact__label">' . esc_html( $r['fact_label'] ?? '' ) . '</span><div class="fact__value">' . $value . $note . '</div>' . $tag . '</div>';
	}
	echo '</div>';
}

// Closing photo banner. Used by the Closing banner section and by the coach and news templates.
function tvbc_band( $image, $heading, $accent, $link_1, $link_2, $classes = '' ) {
	if ( ! $image ) {
		return;
	}
	echo '<section class="band' . ( $classes ? ' ' . esc_attr( $classes ) : '' ) . '">';
	section_image( 'hero', $image, 'band__image', false, true, null, false, '' );
	echo '<div class="band__inner">';
	echo '<h2 class="band__title fade-up">' . tvbc_heading( $heading, $accent ) . '</h2>';
	echo '<div class="band__ctas">' . tvbc_btn( $link_1, 'btn--sun' ) . tvbc_btn( $link_2, 'btn--ghost' ) . '</div>';
	echo '</div></section>';
}

?>
