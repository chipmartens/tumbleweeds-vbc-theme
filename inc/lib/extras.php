<?php

// Set fallback menu when no menu exists
function header_menu_cb() { ?>
	<ul class="menu">
		<li><a href="<?php echo admin_url( 'nav-menus.php' ); ?>">Add menu items</a></li>
	</ul>
<?php }

// Add Section class to Body from Page Configuration
add_filter( 'body_class', 'extra_body_classes' );
function extra_body_classes( $classes ) {
	global $post;

	$whitelist = array( 'home', 'blog', 'post', 'page', 'archive', 'single', 'category', 'tax', 'error404', 'admin-bar', 'customize-support' );
	$blacklist = array( 'postid' );

	$classes_new = array();
	foreach ( $classes as $class ) {
		$is_blacklisted = false;
		foreach ( $blacklist as $black ) {
			if ( strpos( $class, $black ) === 0 ) {
				$is_blacklisted = true;
				break;
			}
		}
		if ( ! $is_blacklisted ) {
			foreach ( $whitelist as $white ) {
				if ( strpos( $class, $white ) === 0 ) {
					$classes_new[] = $class;
				}
			}
		}
	}
	$classes = $classes_new;

	if ( isset( $post ) && ! is_home() && ! is_archive() ) {
		$classes[] = $post->post_type . '-' . $post->post_name;
	}

	// State for the CSS: is there an announcement bar, and does the page end in a closing banner.
	if ( function_exists( 'tvbc_announcement' ) && tvbc_announcement() ) {
		$classes[] = 'has-announcement';
	}
	if ( function_exists( 'tvbc_has_closing_band' ) && tvbc_has_closing_band() ) {
		$classes[] = 'has-band';
	}

	return $classes;
}

// Meta description from what the editor already wrote: hero intro, coach summary or post excerpt
add_action( 'wp_head', 'tvbc_meta_description', 5 );
function tvbc_meta_description() {
	if ( ! function_exists( 'get_field' ) ) {
		return;
	}
	$id = tvbc_context_id();
	if ( is_singular( 'coach' ) ) {
		$d = get_field( 'coach_summary', $id );
	} elseif ( is_singular( 'post' ) ) {
		$d = get_the_excerpt( $id );
	} elseif ( $id ) {
		$d = get_field( 'hero_subhead', $id );
	} else {
		$d = '';
	}
	$d = $d ? $d : get_bloginfo( 'description' );
	if ( $d ) {
		echo '<meta name="description" content="' . esc_attr( wp_strip_all_tags( $d ) ) . '">' . "\n";
	}
}

// Straight quotes everywhere, so editor-typed text in a WYSIWYG box looks the same as text in a plain box
add_filter( 'run_wptexturize', '__return_false' );

// Change default Excerpt More
add_filter( 'excerpt_more', 'new_excerpt_more' );
function new_excerpt_more( $more ) {
	return '&hellip;';
}

// Keep "Coaches" lit in the menu on a coach page (the page that lists them is set in Club settings)
add_filter( 'nav_menu_css_class', 'tvbc_menu_ancestor', 10, 3 );
function tvbc_menu_ancestor( $classes, $item, $args ) {
	if ( is_singular( 'coach' ) && function_exists( 'tvbc_opt' ) ) {
		$page = tvbc_opt( 'coaches_page' );
		if ( $page && (int) $item->object_id === (int) ( is_object( $page ) ? $page->ID : $page ) ) {
			$classes[] = 'current-menu-ancestor';
		}
	}
	return $classes;
}

// Add .embed-container div to media
add_filter( 'embed_oembed_html', 'custom_embed_html', 10, 3 );
function custom_embed_html( $html ) {
	return '<div class="embed-container">' . $html . '</div>';
}

// Function to build Feature Image object (same shape as an ACF image array)
function featured_image_obj( $attachment_id = 0, $post_id = null ) {
	if ( ! $attachment_id ) {
		$attachment_id = get_post_thumbnail_id( $post_id );
	}
	if ( ! $attachment_id ) {
		return;
	}

	$images       = array();
	$images['ID'] = $images['id'] = (int) $attachment_id;
	$src          = wp_get_attachment_image_src( $attachment_id, 'full' );
	$images['url']    = $src[0];
	$images['width']  = $src[1];
	$images['height'] = $src[2];
	$images['alt']    = get_post_meta( $attachment_id, '_wp_attachment_image_alt', true );
	$images['mime_type'] = get_post_mime_type( $attachment_id );
	foreach ( get_intermediate_image_sizes() as $size ) {
		$s = wp_get_attachment_image_src( $attachment_id, $size );
		$images['sizes'][ $size ] = $s ? $s[0] : '';
	}

	return $images;
}

// Helper function to get optimized srcset (excluding the full-size original)
function get_image_srcset_filtered( $section_image, $img_size ) {
	if ( ! $section_image || ! isset( $section_image['id'] ) ) {
		return false;
	}

	$id           = $section_image['id'];
	$meta         = wp_get_attachment_metadata( $id );
	$full_width   = isset( $meta['width'] ) ? $meta['width'] : 0;
	$default      = wp_get_attachment_image_srcset( $id, $img_size );

	if ( ! $default || ! $full_width ) {
		return $default;
	}

	$filtered = array();
	foreach ( explode( ', ', $default ) as $entry ) {
		if ( preg_match( '/(\S+)\s+(\d+)w/', $entry, $m ) && (int) $m[2] < $full_width ) {
			$filtered[] = $entry;
		}
	}

	return $filtered ? implode( ', ', $filtered ) : $default;
}

// Function to output a lazysizes image from an ACF image array
// $img_size: registered size name. $img_obj: ACF image array (or sub field 'section_image' when empty).
// $disable_lazyload: true for above-the-fold images (eager + fetchpriority high).
function section_image( $img_size = null, $img_obj = null, $img_classes = '', $img_wrapper = false, $img_srcset = false, $img_data = null, $disable_lazyload = false, $img_alt = null, $img_style = '' ) {
	$blank_image = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';

	$image = empty( $img_obj ) ? get_sub_field( 'section_image' ) : $img_obj;
	if ( ! $image ) {
		return;
	}

	$id = ! empty( $image['id'] ) ? (int) $image['id'] : (int) ( $image['ID'] ?? 0 );

	// Alt text: parameter override > media library alt > title > empty string
	if ( ! is_null( $img_alt ) ) {
		$alt = $img_alt;
	} elseif ( ! empty( $image['alt'] ) ) {
		$alt = $image['alt'];
	} elseif ( ! empty( $image['title'] ) ) {
		$alt = $image['title'];
	} else {
		$alt = '';
	}

	// URL for the named size, else the original
	if ( is_null( $img_size ) || empty( $image['sizes'][ $img_size ] ) ) {
		$url = $image['url'];
	} else {
		$url = $image['sizes'][ $img_size ];
	}
	if ( empty( $url ) ) {
		return;
	}

	$ratio  = ( ! empty( $image['width'] ) && ! empty( $image['height'] ) ) ? round( $image['width'] / $image['height'], 3 ) : null;
	$srcset = ( $img_srcset && $id ) ? get_image_srcset_filtered( array( 'id' => $id ), $img_size ?: 'large' ) : '';

	$sizes_map = array(
		'hero'     => '100vw',
		'sheet'    => '(max-width: 767px) 100vw, 40vw',
		'sheet-sm' => '(max-width: 767px) 100vw, 25vw',
	);
	$sizes = isset( $sizes_map[ $img_size ] ) ? $sizes_map[ $img_size ] : 'auto';

	$data_out = $img_style ? ' style="' . esc_attr( $img_style ) . '"' : '';
	if ( is_array( $img_data ) ) {
		foreach ( $img_data as $k => $v ) {
			$data_out .= ' data-' . esc_attr( $k ) . '="' . esc_attr( $v ) . '"';
		}
	}

	if ( 'image/svg+xml' === ( $image['mime_type'] ?? '' ) ) {
		echo '<img' . ( $img_classes ? ' class="' . esc_attr( $img_classes ) . '"' : '' ) . ' src="' . esc_url( $url ) . '" alt="' . esc_attr( $alt ) . '"' . $data_out . ' loading="lazy" decoding="async">';
		return;
	}

	if ( $disable_lazyload ) {
		// Above the fold: eager, high priority
		echo '<img class="' . esc_attr( trim( $img_classes ) ) . '" src="' . esc_url( $url ) . '" alt="' . esc_attr( $alt ) . '"'
			. ( $srcset ? ' srcset="' . esc_attr( $srcset ) . '" sizes="' . esc_attr( $sizes ) . '"' : '' )
			. ( $ratio ? ' data-aspectratio="' . esc_attr( $ratio ) . '"' : '' )
			. $data_out . ' loading="eager" fetchpriority="high" decoding="async">';
		return;
	}

	$tag = '<img class="' . esc_attr( trim( $img_classes . ' lazyload' ) ) . '" src="' . esc_url( $blank_image ) . '" data-src="' . esc_url( $url ) . '" alt="' . esc_attr( $alt ) . '"'
		. ( $srcset ? ' data-srcset="' . esc_attr( $srcset ) . '" data-sizes="' . esc_attr( $sizes ) . '"' : '' )
		. ( $ratio ? ' data-aspectratio="' . esc_attr( $ratio ) . '"' : '' )
		. $data_out . ' loading="lazy" decoding="async">';

	if ( $img_wrapper && $ratio ) {
		echo '<div class="lazyload-image-wrapper" style="padding-top:' . esc_attr( ( 1 / $ratio ) * 100 ) . '%">' . $tag . '</div>';
	} else {
		echo $tag;
	}
}

/**
 * Text and markup utilities. Every output helper escapes.
 */

// Heading text + optional italic accent words at the end (two plain fields, no syntax)
function tvbc_heading( $main, $accent = '' ) {
	$out = esc_html( (string) $main );
	if ( $accent ) {
		$out .= ' <span class="accent">' . esc_html( $accent ) . '</span>';
	}
	return $out;
}

// object-position value from two 0-100 slider values (which part of a cropped photo stays in view)
// $phone = optional array( x, y ) for a different framing on a phone (the CSS reads --focus and --focus-phone)
function tvbc_focus( $x, $y, $phone = null ) {
	$pos = function ( $a, $b ) {
		$a = ( '' === $a || null === $a ) ? 50 : max( 0, min( 100, (int) $a ) );
		$b = ( '' === $b || null === $b ) ? 50 : max( 0, min( 100, (int) $b ) );
		return $a . '% ' . $b . '%';
	};
	$css = '--focus:' . $pos( $x, $y ) . ';';
	if ( is_array( $phone ) ) {
		$css .= '--focus-phone:' . $pos( $phone[0], $phone[1] ) . ';';
	}
	return $css;
}

// Phone number to a tel: value. Handles letters (1-888-83SPORT) and a trailing (77678) alias.
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

// Plain text from a field: escaped, web and email addresses clickable, line breaks kept.
function tvbc_text( $s ) {
	$s = trim( (string) $s );
	if ( '' === $s ) {
		return '';
	}
	$html = make_clickable( esc_html( $s ) );
	$html = str_replace( '<a href=', '<a class="link" href=', $html );
	return nl2br( $html );
}

// Inline SVG icons used in several places
function tvbc_icon( $name ) {
	$icons = array(
		'arrow' => '<svg class="arrow" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>',
		'plus'  => '<span class="faq__icon"><svg width="14" height="14" viewBox="0 0 14 14" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M7 1v12M1 7h12"/></svg></span>',
		'menu'  => '<svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M2 6h14M2 12h14"/></svg>',
		'close' => '<svg width="16" height="16" viewBox="0 0 16 16" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M2 2l12 12M14 2L2 14"/></svg>',
	);
	return isset( $icons[ $name ] ) ? $icons[ $name ] : '';
}

// Theme image URL (logo marks live in assets/img, compiled from src/img)
function tvbc_theme_img( $file ) {
	return get_template_directory_uri() . '/assets/img/' . ltrim( $file, '/' );
}

// The club mark (the traced tumbleweed). Club settings can replace it; the default ships in assets/img.
// $reverse = for dark backgrounds. A replaced logo has one colour only, so on dark it is tinted white by CSS.
function tvbc_mark( $reverse = false, $class = '', $size = 40 ) {
	$custom = function_exists( 'tvbc_opt' ) ? tvbc_opt( 'logo_mark' ) : '';
	if ( ! empty( $custom['url'] ) ) {
		$src   = $custom['url'];
		$class = trim( $class . ( $reverse ? ' is-tinted' : '' ) );
	} else {
		$src = tvbc_theme_img( $reverse ? 'tumbleweeds-mark-reverse.svg' : 'tumbleweeds-mark.svg' );
	}
	return '<img' . ( $class ? ' class="' . esc_attr( $class ) . '"' : '' ) . ' src="' . esc_url( $src ) . '" alt="" width="' . (int) $size . '" height="' . (int) $size . '">';
}

// Browser tab icon: the one set in Club settings, else the Site Icon from the Customizer, else the club mark
function tvbc_favicon() {
	$fav = function_exists( 'tvbc_opt' ) ? tvbc_opt( 'favicon' ) : '';
	if ( ! empty( $fav['url'] ) ) {
		echo '<link rel="icon" href="' . esc_url( $fav['url'] ) . '">' . "\n";
	} elseif ( ! has_site_icon() ) {
		echo '<link rel="icon" type="image/svg+xml" href="' . esc_url( tvbc_theme_img( 'tumbleweeds-mark.svg' ) ) . '">' . "\n";
	}
}

// ACF link array to a button: <a class="btn btn--style">Label</a>. '' when the link is empty.
function tvbc_btn( $link, $classes = 'btn--dark', $arrow = false ) {
	if ( empty( $link['url'] ) ) {
		return '';
	}
	$target = ! empty( $link['target'] ) ? ' target="' . esc_attr( $link['target'] ) . '" rel="noopener"' : '';
	return '<a class="btn ' . esc_attr( $classes ) . '" href="' . esc_url( $link['url'] ) . '"' . $target . '>' . esc_html( $link['title'] ) . ( $arrow ? ' ' . tvbc_icon( 'arrow' ) : '' ) . '</a>';
}

// ACF link array to an inline arrow link: <a class="link">Label ></a>
function tvbc_link( $link ) {
	if ( empty( $link['url'] ) ) {
		return '';
	}
	$target = ! empty( $link['target'] ) ? ' target="' . esc_attr( $link['target'] ) . '" rel="noopener"' : '';
	return '<a class="link" href="' . esc_url( $link['url'] ) . '"' . $target . '>' . esc_html( $link['title'] ) . ' ' . tvbc_icon( 'arrow' ) . '</a>';
}

// Status tag, e.g. "Coming soon"
function tvbc_tag( $text ) {
	return $text ? '<span class="tag tag--soon">' . esc_html( $text ) . '</span>' : '';
}

// Small fixed UI strings, in one place. Page content never goes here.
function tvbc_ui( $key ) {
	static $ui = array(
		'skip'       => 'Skip to content',
		'menu_open'  => 'Open menu',
		'menu_close' => 'Close menu',
		'read_bio'   => 'Read the bio',
		'all_coaches' => 'All coaches',
		'all_news'   => 'All news',
		'read_more'  => 'Read more',
		'next'       => 'Next',
		'prev'       => 'Previous',
		'email_ph'   => 'Your email',
		'form_name'  => 'Your name',
		'form_email' => 'Your email',
		'form_topic' => 'What is it about',
		'form_msg'   => 'Message',
		'form_send'  => 'Send message',
		'sign_up'    => 'Sign up',
		'no_news'    => 'No news yet.',
		'e404_tag'   => '404',
		'e404_title' => 'That page is not here.',
		'e404_text'  => 'Try the menu above, or head back to the home page.',
		'e404_btn'   => 'Back home',
	);
	return isset( $ui[ $key ] ) ? $ui[ $key ] : '';
}

?>
