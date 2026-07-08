<?php
/**
 * מדריך בודד (post). קישור פנימי לשירותים + CTA.
 *
 * @package niv
 */

get_header();

while ( have_posts() ) : the_post(); ?>
	<main id="niv-main">
		<div class="niv-container"><?php niv_breadcrumbs(); ?></div>

		<article class="niv-section">
			<div class="niv-container niv-prose">
				<h1><?php the_title(); ?></h1>
				<?php if ( has_post_thumbnail() ) : the_post_thumbnail( 'niv_hero', array( 'style' => 'border-radius:var(--niv-radius-lg);margin-block:1rem' ) ); endif; ?>
				<?php the_content(); ?>
			</div>
		</article>

		<!-- CTA באמצע/סוף המדריך -->
		<section class="niv-section niv-cta-strip">
			<div class="niv-container niv-narrow">
				<h2>נתקעתם עם דלת או מנעול?</h2>
				<p>אל תתמודדו לבד. התקשרו לניב ותקבלו כיוון כבר בשיחה.</p>
				<div class="niv-btn-row">
					<?php niv_call_button( array( 'location' => 'guide-cta', 'text' => niv_has_phone() ? niv_phone_display() : 'חייגו עכשיו', 'class' => 'niv-btn--lg' ) ); ?>
					<?php niv_whatsapp_button( array( 'location' => 'guide-cta', 'class' => 'niv-btn--lg niv-btn--ghost-light' ) ); ?>
				</div>
			</div>
		</section>

		<!-- מדריכים קשורים -->
		<?php
		$related = get_posts( array( 'numberposts' => 3, 'post__not_in' => array( get_the_ID() ), 'post_status' => 'publish' ) );
		if ( $related ) : ?>
		<section class="niv-section">
			<div class="niv-container">
				<div class="niv-section__head"><h2>עוד מדריכים</h2></div>
				<div class="niv-cards">
					<?php foreach ( $related as $r ) : ?>
						<article class="niv-card">
							<h3><a href="<?php echo esc_url( get_permalink( $r ) ); ?>"><?php echo esc_html( get_the_title( $r ) ); ?></a></h3>
							<a class="niv-card__link" href="<?php echo esc_url( get_permalink( $r ) ); ?>">לקריאה ‹</a>
						</article>
					<?php endforeach; ?>
				</div>
			</div>
		</section>
		<?php endif; ?>
	</main>
<?php endwhile; get_footer(); ?>
