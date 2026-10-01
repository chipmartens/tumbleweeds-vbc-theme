<?php
// Helpers used by template-parts/content-flexcontent.php and content-hero.php.
// Every output helper escapes. Square-bracket text such as [Fee: $TBC] is shown as a highlighted placeholder.

/** Wrap [bracketed placeholders] so open facts are visible on the page. Input must already be escaped. */
function tvbc_ph( $html ) {
	return preg_replace( '/\[([^\[\]<>]{1,90})\]/u', '<mark class="ph">[$1]</mark>', $html );
}

/** Swap {info_date} and {info_details} for the Club settings values (one place to update after the event). */
function tvbc_tokens( $s ) {
	if ( false === strpos( (string) $s, '{info_' ) ) {
		return $s;
	}
	return strtr( $s, array(
		'{info_date}'    => tvbc_opt( 'info_session_date' ) ?: '[Info session date TBC]',
		'{info_details}' => tvbc_opt( 'info_session_details' ) ?: '[Info session details TBC]',
	) );
}
add_filter( 'the_content', 'tvbc_tokens', 9 );

/** One line of plain text, escaped, placeholders highlighted. */
function tvbc_inline( $s ) {
	return tvbc_ph( esc_html( tvbc_tokens( (string) $s ) ) );
}

/** Phone number to a tel: value. Handles letters (1-888-83SPORT) and a trailing (77678) alias. */
function tvbc_tel( $s ) {
	$s   = preg_replace( '/\(.*?\)/', '', (string) $s );
	$map = array( 'ABC' => 2, 'DEF' => 3, 'GHI' => 4, 'JKL' => 5, 'MNO' => 6, 'PQRS' => 7, 'TUV' => 8, 'WXYZ' => 9 );
	$out = '';
	foreach ( str_split( strtoupper( $s ) ) as $ch ) {
		if ( ctype_digit( $ch ) ) {
			$out .= $ch;
		} elseif ( ctype_alpha( $ch ) ) {
			foreach ( $map as $letters => $d ) {
				if ( false !== strpos( $letters, $ch ) ) {
					$out .= $d;
				}
			}
		}
	}
	return '+' . $out;
}

/** Paragraph text: escaped, links and emails clickable, phone numbers as tel: links, placeholders highlighted, wpautop. */
function tvbc_rich( $s ) {
	$s = trim( tvbc_tokens( (string) $s ) );
	if ( '' === $s ) {
		return '';
	}
	$html = make_clickable( esc_html( $s ) );
	$html = preg_replace_callback( '/(?<![\d>"+-])1-\d{3}-(?:\d{3}-\d{4}|\d{2}[A-Z]{5})(?: \(\d{5}\))?/', function ( $m ) {
		return '<a href="tel:' . tvbc_tel( $m[0] ) . '">' . $m[0] . '</a>';
	}, $html );
	return wpautop( tvbc_ph( $html ) );
}

/** Settings value. Reads the Club settings options page when it exists, else the front page (free fields plugin). */
function tvbc_opt( $name ) {
	static $defaults = array(
		'contact_email'      => 'info@tumbleweedsvolleyball.com',
		'instagram_handle'   => '@tumbleweedsvball',
		'instagram_url'      => 'https://www.instagram.com/tumbleweedsvball/',
		'header_cta_label'   => 'Tryouts',
		'helpline_name'      => 'Abuse-Free Sport Helpline',
		'helpline_phone'     => '1-888-83SPORT (77678)',
		'complaints_contact' => '[Complaints contact TBC]',
		'practice_location'  => '[Practice location TBC]',
		'footer_blurb'       => '',
		'info_session_date'    => 'Sunday, October 4',
		'info_session_details' => '7:00 to 8:30 pm, TRU Science Building S337',
		'status_line'          => 'A Volleyball BC member club in good standing (new club), Zone 2 Thompson-Okanagan.',
		'location_line'        => 'Kamloops, BC',
	);
	if ( ! function_exists( 'get_field' ) ) {
		return isset( $defaults[ $name ] ) ? $defaults[ $name ] : '';
	}
	$v = function_exists( 'acf_add_options_page' ) ? get_field( $name, 'option' ) : get_field( $name, (int) get_option( 'page_on_front' ) );
	if ( empty( $v ) && isset( $defaults[ $name ] ) ) {
		return $defaults[ $name ];
	}
	return $v;
}

/** URL for an ACF link array, or '' . */
function tvbc_url( $link ) {
	return ( is_array( $link ) && ! empty( $link['url'] ) ) ? $link['url'] : '';
}

/** Button or link. $style: main | sun | line | plain. */
function tvbc_btn( $label, $link, $style = 'main' ) {
	$url = tvbc_url( $link );
	if ( '' === trim( (string) $label ) || '' === $url ) {
		return '';
	}
	$target = ( ! empty( $link['target'] ) ) ? ' target="' . esc_attr( $link['target'] ) . '" rel="noopener"' : '';
	return '<a class="btn btn--' . esc_attr( $style ) . '" href="' . esc_url( $url ) . '"' . $target . '>' . tvbc_inline( $label ) . '</a>';
}

/** Responsive image from an attachment id. */
function tvbc_img( $id, $class = '', $size = 'large' ) {
	if ( ! $id ) {
		return '';
	}
	return wp_get_attachment_image( (int) $id, $size, false, array( 'class' => $class, 'loading' => 'lazy' ) );
}

/** The branch pattern from the logo, drawn as a CSS mask so any token colour can fill it. Decorative. */
function tvbc_pattern( $class = '' ) {
	return '<span class="pattern ' . esc_attr( $class ) . '" aria-hidden="true"></span>';
}

/** Section id: the editor's Link name if set, else section-N. */
function tvbc_section_id( $i ) {
	$a = sanitize_title( (string) get_sub_field( 'anchor' ) );
	return $a ? $a : 'section-' . (int) $i;
}

/** Background modifier class from the Background field. */
function tvbc_bg_class( $bg ) {
	$bg = in_array( $bg, array( 'light', 'sand', 'dark' ), true ) ? $bg : 'light';
	return 'section--' . $bg;
}

/** Eyebrow + heading + intro, the same head on every section. */
function tvbc_section_head( $align = '' ) {
	$eyebrow = get_sub_field( 'eyebrow' );
	$heading = get_sub_field( 'heading' );
	$intro   = get_sub_field( 'intro' );
	if ( ! $eyebrow && ! $heading && ! $intro ) {
		return;
	}
	echo '<header class="section__head' . ( $align ? ' section__head--' . esc_attr( $align ) : '' ) . '">';
	if ( $eyebrow ) {
		echo '<p class="eyebrow">' . tvbc_inline( $eyebrow ) . '</p>';
	}
	if ( $heading ) {
		echo '<h2 class="section__heading">' . tvbc_inline( $heading ) . '</h2>';
	}
	if ( $intro ) {
		echo '<div class="section__intro">' . tvbc_rich( $intro ) . '</div>';
	}
	echo '</header>';
}
