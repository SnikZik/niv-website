<?php
/**
 * ארכיון אזורי שירות — גריד ערים/שכונות.
 *
 * @package niv
 */

get_header(); ?>
<main id="niv-main">
	<div class="niv-container"><?php niv_breadcrumbs(); ?></div>
	<section class="niv-section">
		<div class="niv-container">
			<div class="niv-section__head">
				<h1>אזורי שירות — מנעולן בירושלים והסביבה</h1>
				<p>בחרו את האזור שלכם כדי לראות פרטים על שירותי מנעולן במקום.</p>
			</div>
			<div class="niv-areas">
				<?php while ( have_posts() ) : the_post(); ?>
					<a class="niv-area-chip js-area-card" data-area="<?php echo esc_attr( get_the_title() ); ?>" href="<?php the_permalink(); ?>">
						<?php echo niv_icon( 'home' ); ?>מנעולן ב<?php echo esc_html( get_field( 'area_name' ) ?: get_the_title() ); ?>
					</a>
				<?php endwhile; ?>
			</div>
		</div>
	</section>

	<section class="niv-section niv-cta-strip">
		<div class="niv-container niv-narrow">
			<h2>צריכים מנעולן עכשיו?</h2>
			<div class="niv-btn-row">
				<?php niv_call_button( array( 'location' => 'archive-area-cta', 'text' => niv_has_phone() ? niv_phone_display() : 'חייגו עכשיו', 'class' => 'niv-btn--lg' ) ); ?>
				<?php niv_whatsapp_button( array( 'location' => 'archive-area-cta', 'class' => 'niv-btn--lg niv-btn--ghost-light' ) ); ?>
			</div>
		</div>
	</section>
</main>
<?php get_footer(); ?>
