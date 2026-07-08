<?php
/**
 * עמוד אזור שירות (עיר/שכונה). H1 = מנעולן ב{אזור}.
 *
 * @package niv
 */

get_header();

while ( have_posts() ) : the_post();
	$area_name = get_field( 'area_name' ) ?: get_the_title();
	$intro     = get_field( 'local_intro' );
	$avail     = get_field( 'availability_text' );
	$services  = get_field( 'services_available' );
	$nearby    = get_field( 'nearby_areas' );
	$faq       = get_field( 'faq' );

	// עמודי שירות×אזור השייכים לאזור הזה.
	$sap = get_posts( array(
		'post_type' => 'service_area_page', 'numberposts' => 12, 'post_status' => 'publish',
		'meta_query' => array( array( 'key' => 'area_ref', 'value' => '"' . get_the_ID() . '"', 'compare' => 'LIKE' ) ),
	) );
	?>

	<main id="niv-main">
		<div class="niv-container"><?php niv_breadcrumbs(); ?></div>

		<section class="niv-hero">
			<?php if ( has_post_thumbnail() ) : ?>
				<div class="niv-hero__media"><?php the_post_thumbnail( 'niv_hero', array( 'alt' => esc_attr( 'מנעולן ב' . $area_name ) ) ); ?></div>
			<?php endif; ?>
			<div class="niv-container niv-hero__inner">
				<div class="niv-hero__content">
					<h1>מנעולן ב<?php echo esc_html( $area_name ); ?></h1>
					<p class="niv-hero__sub"><?php echo esc_html( $avail ?: 'מענה לתקלות דלתות, צילינדרים ומנעולים באזור ' . $area_name . ' והסביבה.' ); ?></p>
					<div class="niv-btn-row">
						<?php niv_call_button( array( 'location' => 'area-hero', 'text' => 'חייגו עכשיו', 'class' => 'niv-btn--lg' ) ); ?>
						<?php niv_whatsapp_button( array( 'location' => 'area-hero', 'class' => 'niv-btn--lg' ) ); ?>
					</div>
				</div>
			</div>
		</section>

		<section class="niv-section">
			<div class="niv-container niv-prose">
				<?php if ( $intro ) : echo wp_kses_post( $intro ); else : the_content(); endif; ?>
			</div>
		</section>

		<?php if ( $sap ) : ?>
		<section class="niv-section niv-section--alt">
			<div class="niv-container">
				<div class="niv-section__head"><h2>שירותי מנעולן ב<?php echo esc_html( $area_name ); ?></h2></div>
				<div class="niv-cards">
					<?php foreach ( $sap as $p ) : ?>
						<article class="niv-card">
							<h3><a href="<?php echo esc_url( get_permalink( $p ) ); ?>"><?php echo esc_html( get_the_title( $p ) ); ?></a></h3>
							<a class="niv-card__link" href="<?php echo esc_url( get_permalink( $p ) ); ?>">לפרטים ‹</a>
						</article>
					<?php endforeach; ?>
				</div>
			</div>
		</section>
		<?php elseif ( $services ) : ?>
		<section class="niv-section niv-section--alt">
			<div class="niv-container">
				<div class="niv-section__head"><h2>שירותים זמינים ב<?php echo esc_html( $area_name ); ?></h2></div>
				<div class="niv-cards">
					<?php foreach ( $services as $s ) : ?>
						<article class="niv-card">
							<h3><a href="<?php echo esc_url( get_permalink( $s ) ); ?>"><?php echo esc_html( get_the_title( $s ) ); ?></a></h3>
							<p><?php echo esc_html( get_field( 'short_desc', is_object( $s ) ? $s->ID : $s ) ); ?></p>
						</article>
					<?php endforeach; ?>
				</div>
			</div>
		</section>
		<?php endif; ?>

		<?php if ( $faq ) : ?>
		<section class="niv-section"><div class="niv-container"><?php niv_render_faq( $faq ); ?></div></section>
		<?php endif; ?>

		<?php if ( $nearby ) : ?>
		<section class="niv-section niv-section--alt">
			<div class="niv-container">
				<div class="niv-section__head"><h2>אזורים סמוכים</h2></div>
				<div class="niv-areas">
					<?php foreach ( $nearby as $n ) : ?>
						<a class="niv-area-chip js-area-card" data-area="<?php echo esc_attr( get_the_title( $n ) ); ?>" href="<?php echo esc_url( get_permalink( $n ) ); ?>"><?php echo niv_icon( 'home' ); ?><?php echo esc_html( get_the_title( $n ) ); ?></a>
					<?php endforeach; ?>
				</div>
			</div>
		</section>
		<?php endif; ?>

		<section class="niv-section niv-cta-strip">
			<div class="niv-container niv-narrow">
				<h2>צריכים מנעולן ב<?php echo esc_html( $area_name ); ?>?</h2>
				<div class="niv-btn-row">
					<?php niv_call_button( array( 'location' => 'area-cta', 'text' => niv_has_phone() ? niv_phone_display() : 'חייגו עכשיו', 'class' => 'niv-btn--lg' ) ); ?>
					<?php niv_whatsapp_button( array( 'location' => 'area-cta', 'class' => 'niv-btn--lg niv-btn--ghost-light' ) ); ?>
				</div>
			</div>
		</section>
	</main>

<?php endwhile; get_footer(); ?>
