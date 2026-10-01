<?php

// The posts page (News) holds its sections on the page assigned as the posts page.
$flex_post_id = tvbc_context_id();

// Part: Flexible Content
if( have_rows('flex_content', $flex_post_id) ):

	$total_rows = count( get_field('flex_content', $flex_post_id) );
	$i = 1;

	// loop through the rows of data
	while ( have_rows('flex_content', $flex_post_id) ) : the_row();

		// Layout for "Section Ticker" layout type (the words come from Club settings)
		if (get_row_layout() == 'section_ticker'):
			$ticker_phrases = tvbc_opt( 'ticker_phrases' );
		?>

		<?php if ( $ticker_phrases ) : ?>
		<section id="<?php section_id($i); ?>" class="ticker<?php is_last_row($i,$total_rows); ?>" aria-hidden="true">

			<div class="ticker__track">
				<?php for ( $t = 0; $t < 2; $t++ ) : foreach ( $ticker_phrases as $phrase ) : ?>
				<span class="ticker__item"><?php echo esc_html( $phrase['ticker_phrase'] ); ?></span><?php echo tvbc_mark( false, 'ticker__mark', 30 ); // phpcs:ignore ?>
				<?php endforeach; endfor; ?>
			</div>

		</section>
		<?php endif; ?>

		<?php

		// Layout for "Section Cards" layout type
		elseif (get_row_layout() == 'section_cards'):
			$cards        = get_sub_field( 'cards' );
			$card_count   = is_array( $cards ) ? count( $cards ) : 0;
			$cards_grid   = ( 2 === $card_count ) ? '2' : ( ( 5 === $card_count ) ? '5' : '3' );
			$show_numbers = (bool) get_sub_field( 'show_card_numbers' );
			$dates        = get_sub_field( 'cards_dates' ) ? get_sub_field( 'dates' ) : array();
			$info         = tvbc_info_session();
			$date_items   = array();
			if ( is_array( $dates ) ) {
				foreach ( $dates as $d ) {
					if ( 'info_session' === $d['date_kind'] ) {
						if ( ! $info ) { continue; }
						$d['date_label'] = $info['short'];
						$d['date_title'] = $info['title'];
						$d['date_line']  = trim( $info['time'] . ( $info['time'] && $info['place'] ? ', ' : '' ) . $info['place'] );
					}
					$date_items[] = $d;
				}
			}
		?>

		<section id="<?php section_id($i); ?>" class="cards surface<?php section_bg_color(); is_last_row($i,$total_rows); ?>">

			<div class="container-2xl">

				<?php if ( $date_items ) : ?>
				<div class="upnext fade-up" aria-label="<?php esc_attr_e( 'Coming up', 'tvbc' ); ?>">
					<?php foreach ( $date_items as $d ) :
						$href = ! empty( $d['date_link']['url'] ) ? $d['date_link']['url'] : '#'; ?>
					<a class="upnext__item" href="<?php echo esc_url( $href ); ?>">
						<span class="upnext__label"><?php echo esc_html( $d['date_label'] ); ?></span>
						<strong class="upnext__title"><?php echo esc_html( $d['date_title'] ); ?></strong>
						<span class="upnext__line"><?php echo esc_html( $d['date_line'] ); ?></span>
					</a>
					<?php endforeach; ?>
				</div>
				<?php endif; ?>

				<?php section_head(); ?>

				<?php if ( $card_count ) : ?>
				<div class="cards__grid cards__grid--<?php echo esc_attr( $cards_grid ); ?>">
					<?php foreach ( $cards as $ci => $card ) :
						$colour = in_array( $card['card_colour'], array( 'sage', 'sun', 'sand' ), true ) ? $card['card_colour'] : 'sage';
						$foot   = $card['card_foot'];
					?>
					<article class="card card--<?php echo esc_attr( $colour ); ?> fade-up">
						<?php if ( $card['card_image'] ) : ?>
						<div class="card__media"><?php section_image( 'sheet-sm', $card['card_image'], 'card__image', false, true ); ?></div>
						<?php endif; ?>
						<div class="card__body">
							<?php if ( $show_numbers ) : ?><span class="card__num"><?php echo esc_html( sprintf( '%02d', $ci + 1 ) ); ?></span><?php endif; ?>
							<h3 class="card__title"><?php echo esc_html( $card['card_title'] ); ?></h3>
							<?php if ( $card['card_text'] ) : ?><p class="card__text"><?php echo esc_html( $card['card_text'] ); ?></p><?php endif; ?>
							<?php if ( 'tag' === $foot && $card['card_foot_tag'] ) : ?>
							<div class="card__foot"><?php echo tvbc_tag( $card['card_foot_tag'] ); // phpcs:ignore ?></div>
							<?php elseif ( 'link' === $foot && ! empty( $card['card_foot_link']['url'] ) ) : ?>
							<div class="card__foot"><?php echo tvbc_link( $card['card_foot_link'] ); // phpcs:ignore ?></div>
							<?php elseif ( 'button' === $foot && ! empty( $card['card_foot_link']['url'] ) ) : ?>
							<div class="card__foot"><?php echo tvbc_btn( $card['card_foot_link'], 'btn--outline btn--sm' ); // phpcs:ignore ?></div>
							<?php endif; ?>
						</div>
					</article>
					<?php endforeach; ?>
				</div>
				<?php endif; ?>

			</div>

		</section>

		<?php

		// Layout for "Section Strip" layout type (four photos)
		elseif (get_row_layout() == 'section_strip'):
			$strip_photos = get_sub_field( 'strip_photos' );
		?>

		<?php if ( $strip_photos ) : ?>
		<section id="<?php section_id($i); ?>" class="strip<?php is_last_row($i,$total_rows); ?>" aria-label="<?php esc_attr_e( 'Photos', 'tvbc' ); ?>">

			<?php foreach ( $strip_photos as $photo ) : ?>
			<figure class="strip__item fade-up">
				<?php section_image( 'sheet', $photo['strip_image'], 'strip__image', false, true, null, false, null, tvbc_focus( $photo['focus_x'], $photo['focus_y'] ) ); ?>
			</figure>
			<?php endforeach; ?>

		</section>
		<?php endif; ?>

		<?php

		// Layout for "Section People" layout type (coaches come from the Coaches menu)
		elseif (get_row_layout() == 'section_people'):
			$people_ids = get_sub_field( 'people_coaches' );
			$people     = tvbc_coaches_query( $people_ids ? $people_ids : array() );
		?>

		<section id="<?php section_id($i); ?>" class="people surface<?php section_bg_color(); is_last_row($i,$total_rows); ?>">

			<div class="container-2xl">

				<?php section_head(); ?>

				<?php if ( $people->have_posts() ) : ?>
				<div class="people__list">
					<?php while ( $people->have_posts() ) : $people->the_post();
						$p_id    = get_the_ID();
						$p_photo = get_field( 'coach_photo', $p_id );
					?>
					<article class="person fade-up">
						<div class="person__media">
							<?php section_image( 'sheet', $p_photo, 'person__image', false, true, null, false, get_the_title() ); ?>
						</div>
						<div class="person__body">
							<h3 class="person__name"><?php the_title(); ?></h3>
							<span class="person__role"><?php echo esc_html( get_field( 'coach_role', $p_id ) ); ?></span>
							<p class="person__text"><?php echo esc_html( get_field( 'coach_summary', $p_id ) ); ?></p>
							<a class="link" href="<?php the_permalink(); ?>"><?php echo esc_html( tvbc_ui( 'read_bio' ) ); ?> <?php echo tvbc_icon( 'arrow' ); // phpcs:ignore ?></a>
						</div>
					</article>
					<?php endwhile; wp_reset_postdata(); ?>
				</div>
				<?php endif; ?>

			</div>

		</section>

		<?php

		// Layout for "Section Statement" layout type
		elseif (get_row_layout() == 'section_statement'):
		?>

		<section id="<?php section_id($i); ?>" class="statement fade-up<?php is_last_row($i,$total_rows); ?>">

			<?php echo tvbc_mark( false, 'statement__mark', 720 ); // phpcs:ignore ?>

			<p class="statement__text"><?php echo tvbc_heading( get_sub_field( 'section_heading' ), get_sub_field( 'section_heading_accent' ) ); // phpcs:ignore ?></p>

		</section>

		<?php

		// Layout for "Section Events" layout type
		elseif (get_row_layout() == 'section_events'):
			$events = get_sub_field( 'events' );
			$info   = tvbc_info_session();
		?>

		<section id="<?php section_id($i); ?>" class="events surface<?php section_bg_color(); is_last_row($i,$total_rows); ?>">

			<div class="container-2xl">

				<?php section_head(); ?>

				<?php if ( $events ) : ?>
				<div class="events__list">
					<?php foreach ( $events as $ev ) :
						if ( 'info_session' === $ev['event_kind'] ) {
							if ( ! $info ) { continue; }
							$ev_date  = $info['short'];
							$ev_title = $info['title'];
							$ev_text  = trim( $info['time'] . ( $info['time'] && $info['place'] ? ', ' : '' ) . $info['place'] . ( $info['place'] || $info['time'] ? '. ' : '' ) . $info['details'] );
						} else {
							$ev_date  = $ev['event_date'];
							$ev_title = $ev['event_title'];
							$ev_text  = $ev['event_text'];
						}
					?>
					<div class="event fade-up">
						<span class="event__date"><?php echo esc_html( $ev_date ); ?></span>
						<div class="event__body">
							<h3 class="event__title"><?php echo esc_html( $ev_title ); ?></h3>
							<?php if ( $ev_text ) : ?><p class="event__text"><?php echo esc_html( $ev_text ); ?></p><?php endif; ?>
						</div>
						<?php if ( 'tag' === $ev['event_side'] ) : echo tvbc_tag( $ev['event_side_tag'] ); // phpcs:ignore
						elseif ( 'button' === $ev['event_side'] ) : echo tvbc_btn( $ev['event_side_link'], 'btn--outline btn--sm' ); // phpcs:ignore
						endif; ?>
					</div>
					<?php endforeach; ?>
				</div>
				<?php endif; ?>

			</div>

		</section>

		<?php

		// Layout for "Section FAQ" layout type
		elseif (get_row_layout() == 'section_faq'):
			$faq_items      = get_sub_field( 'faq_items' );
			$faq_numbered   = (bool) get_sub_field( 'faq_numbered' );
			$faq_open_first = (bool) get_sub_field( 'faq_open_first' );
		?>

		<section id="<?php section_id($i); ?>" class="faq surface<?php section_bg_color(); is_last_row($i,$total_rows); ?>">

			<div class="container-2xl faq__inner">

				<div class="faq__col faq__col--meta fade-up">
					<?php section_meta( array( 'container_class' => 'faq__meta', 'lede' => true ) ); ?>
				</div>

				<?php if ( $faq_items ) : ?>
				<div class="faq__col faq__col--list fade-up<?php echo $faq_numbered ? ' faq__col--numbered' : ''; ?>">
					<?php foreach ( $faq_items as $f => $item ) :
						$f_id = sanitize_title( (string) $item['faq_anchor'] );
					?>
					<details class="faq__item"<?php echo $f_id ? ' id="' . esc_attr( $f_id ) . '"' : ''; ?><?php echo ( $faq_open_first && 0 === $f ) ? ' open' : ''; ?>>
						<summary class="faq__question">
							<?php if ( $faq_numbered ) : ?><b class="faq__number"><?php echo esc_html( sprintf( '%02d', $f + 1 ) ); ?></b><?php endif; ?>
							<span class="faq__label"><?php echo esc_html( $item['faq_question'] ); ?></span>
							<?php echo tvbc_icon( 'plus' ); // phpcs:ignore ?>
						</summary>
						<div class="faq__answer<?php echo ( 'facts' === $item['answer_kind'] ) ? ' faq__answer--facts' : ' content'; ?>">
							<?php if ( 'facts' === $item['answer_kind'] ) : tvbc_facts( $item['answer_facts'] );
							else : echo $item['answer_text']; // phpcs:ignore -- WYSIWYG, filtered by WordPress on save
							endif; ?>
						</div>
					</details>
					<?php endforeach; ?>
				</div>
				<?php endif; ?>

			</div>

		</section>

		<?php

		// Layout for "Section CTA" layout type (yellow banner, or a tinted section)
		elseif (get_row_layout() == 'section_cta'):
			$cta_style = get_sub_field( 'cta_style' ) ?: 'banner';
		?>

		<?php if ( 'highlight' === $cta_style ) : ?>
		<section id="<?php section_id($i); ?>" class="cta cta--highlight surface surface--sun<?php is_last_row($i,$total_rows); ?>">

			<div class="container-2xl">

				<div class="surface__head fade-up">
					<div class="meta">
						<?php $cta_num = get_sub_field( 'show_number' ) ? numbered_sections() : ''; ?>
						<p class="section__eyebrow"><?php echo $cta_num ? '<b>' . esc_html( $cta_num ) . '</b>' : ''; ?><?php echo esc_html( get_sub_field( 'section_eyebrow' ) ); ?></p>
						<h2 class="cta__title"><?php echo esc_html( get_sub_field( 'section_heading' ) ); ?></h2>
						<?php if ( get_sub_field( 'section_lede' ) ) : ?>
						<p class="section__subhead"><?php echo esc_html( get_sub_field( 'section_lede' ) ); ?> <?php echo tvbc_tag( get_sub_field( 'cta_tag' ) ); // phpcs:ignore ?></p>
						<?php endif; ?>
					</div>
					<?php section_cta( 'btn--dark' ); ?>
				</div>

			</div>

		</section>
		<?php else : ?>
		<section id="<?php section_id($i); ?>" class="cta cta--banner<?php is_last_row($i,$total_rows); ?>">

			<div class="cta__inner fade-up">
				<div class="meta">
					<p class="section__eyebrow"><?php echo esc_html( get_sub_field( 'section_eyebrow' ) ); ?></p>
					<h2 class="cta__title"><?php echo esc_html( get_sub_field( 'section_heading' ) ); ?></h2>
				</div>
				<?php section_cta( 'btn--dark' ); ?>
			</div>

		</section>
		<?php endif; ?>

		<?php

		// Layout for "Section Facts" layout type
		elseif (get_row_layout() == 'section_facts'):
			$facts_layout = get_sub_field( 'facts_layout' ) ?: 'above';
			$facts_rows   = get_sub_field( 'facts_rows' );
			$box          = get_sub_field( 'facts_box' );
			$chips        = $box ? get_sub_field( 'box_chips' ) : array();
		?>

		<section id="<?php section_id($i); ?>" class="facts surface<?php section_bg_color(); is_last_row($i,$total_rows); ?>">

			<div class="container-2xl<?php echo ( 'left' === $facts_layout ) ? ' facts__split' : ''; ?>">

				<?php if ( 'left' === $facts_layout ) : ?>

				<div class="facts__col facts__col--meta fade-up">
					<?php section_meta( array( 'container_class' => 'facts__meta', 'lede' => true ) ); ?>
				</div>
				<div class="facts__col facts__col--list fade-up">
					<?php tvbc_facts( $facts_rows ); ?>
				</div>

				<?php else : ?>

				<?php section_head(); ?>

				<?php if ( $box ) : ?>
				<div class="highlight fade-up">
					<div class="highlight__text">
						<?php if ( get_sub_field( 'box_eyebrow' ) ) : ?><p class="section__eyebrow"><?php echo esc_html( get_sub_field( 'box_eyebrow' ) ); ?></p><?php endif; ?>
						<h3 class="highlight__title"><?php echo esc_html( get_sub_field( 'box_heading' ) ); ?></h3>
						<?php if ( get_sub_field( 'box_text' ) ) : ?><p class="highlight__lede"><?php echo esc_html( get_sub_field( 'box_text' ) ); ?> <?php echo tvbc_tag( get_sub_field( 'box_tag' ) ); // phpcs:ignore ?></p><?php endif; ?>
					</div>
					<?php if ( $chips ) : ?>
					<div class="chips">
						<?php foreach ( $chips as $chip ) : ?><span class="chip"><?php echo esc_html( $chip['chip_text'] ); ?></span><?php endforeach; ?>
					</div>
					<?php endif; ?>
				</div>
				<?php endif; ?>

				<?php if ( $facts_rows ) : ?>
				<div class="fade-up"><?php tvbc_facts( $facts_rows ); ?></div>
				<?php endif; ?>

				<?php endif; ?>

			</div>

		</section>

		<?php

		// Layout for "Section Ages" layout type
		elseif (get_row_layout() == 'section_ages'):
			$ages = get_sub_field( 'ages' );
		?>

		<section id="<?php section_id($i); ?>" class="ages surface<?php section_bg_color(); is_last_row($i,$total_rows); ?>">

			<div class="container-2xl">

				<?php section_head(); ?>

				<?php if ( $ages ) : ?>
				<div class="ages__grid fade-up">
					<?php foreach ( $ages as $age ) : ?>
					<div class="age"><b class="age__number"><?php echo esc_html( $age['age_label'] ); ?></b><span class="age__caption"><?php echo esc_html( $age['age_caption'] ); ?></span></div>
					<?php endforeach; ?>
				</div>
				<?php endif; ?>

				<?php if ( get_sub_field( 'ages_note' ) ) : ?>
				<p class="ages__note fade-up"><?php echo esc_html( get_sub_field( 'ages_note' ) ); ?> <?php echo tvbc_tag( get_sub_field( 'ages_note_tag' ) ); // phpcs:ignore ?></p>
				<?php endif; ?>

			</div>

		</section>

		<?php

		// Layout for "Section Helpline" layout type (the number comes from Club settings)
		elseif (get_row_layout() == 'section_helpline'):
			list( $help_main, $help_alias ) = tvbc_phone_parts( tvbc_opt( 'helpline_phone' ) );
			$help_num = get_sub_field( 'show_number' ) ? numbered_sections() : '';
		?>

		<section id="<?php section_id($i); ?>" class="helpline fade-up<?php is_last_row($i,$total_rows); ?>">

			<p class="section__eyebrow"><?php echo $help_num ? '<b>' . esc_html( $help_num ) . '</b>' : ''; ?><?php echo esc_html( get_sub_field( 'section_eyebrow' ) ); ?></p>
			<h2 class="helpline__title"><?php echo esc_html( get_sub_field( 'section_heading' ) ); ?></h2>
			<?php if ( get_sub_field( 'section_lede' ) ) : ?><p class="helpline__text"><?php echo esc_html( get_sub_field( 'section_lede' ) ); ?></p><?php endif; ?>
			<?php if ( $help_main ) : ?>
			<a class="helpline__number" href="tel:<?php echo esc_attr( tvbc_tel( $help_main ) ); ?>"><?php echo esc_html( $help_main ); ?><?php echo $help_alias ? '<small>' . esc_html( $help_alias ) . '</small>' : ''; ?></a>
			<?php endif; ?>

		</section>

		<?php

		// Layout for "Section Contact" layout type
		elseif (get_row_layout() == 'section_contact'):
			$topics = get_sub_field( 'form_topics' );
			$mail   = tvbc_opt( 'contact_email' );
		?>

		<section id="<?php section_id($i); ?>" class="contact surface<?php section_bg_color(); is_last_row($i,$total_rows); ?>">

			<div class="container-2xl contact__split">

				<div class="contact__info">
					<div class="fade-up"><?php section_meta( array( 'container_class' => 'contact__meta', 'lede' => true ) ); ?></div>
					<?php tvbc_facts( get_sub_field( 'contact_rows' ), 'fade-up' ); ?>
				</div>

				<div class="contact__panel fade-up">
					<!-- No form plugin: submit opens the visitor's email app with the message filled in. -->
					<form class="form" data-mailto-form data-mailto="<?php echo esc_attr( $mail ); ?>" action="mailto:<?php echo esc_attr( $mail ); ?>" method="post" enctype="text/plain">
						<h3 class="form__title"><?php echo esc_html( get_sub_field( 'form_heading' ) ); ?></h3>
						<label><?php echo esc_html( tvbc_ui( 'form_name' ) ); ?><input name="name" type="text" autocomplete="name" required></label>
						<label><?php echo esc_html( tvbc_ui( 'form_email' ) ); ?><input name="email" type="email" autocomplete="email" required></label>
						<?php if ( $topics ) : ?>
						<label><?php echo esc_html( tvbc_ui( 'form_topic' ) ); ?>
							<select name="topic">
								<?php foreach ( $topics as $topic ) : ?><option><?php echo esc_html( $topic['topic_text'] ); ?></option><?php endforeach; ?>
							</select>
						</label>
						<?php endif; ?>
						<label><?php echo esc_html( tvbc_ui( 'form_msg' ) ); ?><textarea name="message" required></textarea></label>
						<button class="btn btn--dark" type="submit"><?php echo esc_html( tvbc_ui( 'form_send' ) ); ?></button>
						<?php if ( get_sub_field( 'form_note' ) ) : ?><p class="form__note"><?php echo esc_html( get_sub_field( 'form_note' ) ); ?></p><?php endif; ?>
					</form>
				</div>

			</div>

		</section>

		<?php

		// Layout for "Section News" layout type (the cards are the posts)
		elseif (get_row_layout() == 'section_news'):
			$news   = tvbc_news_query( get_sub_field( 'news_count' ) ?: 12 );
			$tints  = array( 'sage', 'sun', 'sand' );
			$n      = 0;
		?>

		<section id="<?php section_id($i); ?>" class="news surface<?php section_bg_color(); is_last_row($i,$total_rows); ?>">

			<div class="container-2xl">

				<?php section_head(); ?>

				<?php if ( $news->have_posts() ) : ?>
				<div class="cards__grid cards__grid--2">
					<?php while ( $news->have_posts() ) : $news->the_post();
						$post_image = featured_image_obj( 0, get_the_ID() );
					?>
					<a class="card card--<?php echo esc_attr( $tints[ $n % 3 ] ); ?> card--link fade-up" href="<?php the_permalink(); ?>">
						<?php if ( $post_image ) : ?><div class="card__media"><?php section_image( 'sheet', $post_image, 'card__image', false, true, null, false, '' ); ?></div><?php endif; ?>
						<div class="card__body">
							<span class="card__meta"><?php echo esc_html( get_the_date( 'M j, Y' ) ); ?></span>
							<h3 class="card__title"><?php the_title(); ?></h3>
							<p class="card__text"><?php echo esc_html( get_the_excerpt() ); ?></p>
							<div class="card__foot"><span class="link"><?php echo esc_html( tvbc_ui( 'read_more' ) ); ?> <?php echo tvbc_icon( 'arrow' ); // phpcs:ignore ?></span></div>
						</div>
					</a>
					<?php $n++; endwhile; wp_reset_postdata(); ?>
				</div>
				<?php else : ?>
				<p class="section__subhead"><?php echo esc_html( tvbc_ui( 'no_news' ) ); ?></p>
				<?php endif; ?>

			</div>

		</section>

		<?php

		// Layout for "Section Band" layout type (closing photo banner)
		elseif (get_row_layout() == 'section_band'):
			tvbc_band(
				get_sub_field( 'band_image' ),
				get_sub_field( 'band_heading' ),
				get_sub_field( 'band_heading_accent' ),
				get_sub_field( 'band_button_1' ),
				get_sub_field( 'band_button_2' ),
				'tall' === get_sub_field( 'band_size' ) ? 'band--tall' : ''
			);

		endif; // flex_content layout

		$i++;

	endwhile; // flex_content

endif; // flex_content
