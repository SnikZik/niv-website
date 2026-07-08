<?php
/**
 * עמוד שירות×אזור (פרוגרמטי). דורש unique_intro (שער thin-content).
 *
 * @package niv
 */

get_header();

while ( have_posts() ) : the_post();
	$ctx        = niv_page_context();
	$h1         = get_field( 'h1' ) ?: get_the_title();
	$hero_text  = get_field( 'hero_text' );
	$intro      = get_field( 'unique_intro' );
	$local      = get_field( 'local_context' );
	$specific   = get_field( 'service_specific' );
	$faq        = get_field( 'faq' );
	$service    = get_field( 'service_ref' );
	$area       = get_field( 'area_ref' );
	$links      = get_field( 'internal_links' );
	?>

	<main id="niv-main">
		<div class="niv-container"><?php niv_breadcrumbs(); ?></div>

		<section class="niv-hero">
			<div class="niv-container niv-hero__inner">
				<div class="niv-hero__content">
					<h1><?php echo esc_html( $h1 ); ?></h1>
					<?php if ( $hero_text ) : ?><p class="niv-hero__sub"><?php echo esc_html( $hero_text ); ?></p><?php endif; ?>
					<div class="niv-btn-row">
						<?php niv_call_button( array( 'location' => 'sap-hero', 'text' => 'חייגו עכשיו', 'class' => 'niv-btn--lg' ) ); ?>
						<?php niv_whatsapp_button( array( 'location' => 'sap-hero', 'class' => 'niv-btn--lg' ) ); ?>
					</div>
				</div>
			</div>
		</section>

		<section class="niv-section">
			<div class="niv-container niv-prose">
				<?php echo wp_kses_post( $intro ); ?>
				<?php if ( $specific ) : ?><h2><?php echo esc_html( $ctx['service'] ?: 'השירות' ); ?></h2><?php echo wp_kses_post( $specific ); endif; ?>
				<?php if ( $local ) : ?><h2>באזור <?php echo esc_html( $ctx['area'] ); ?></h2><?php echo wp_kses_post( $local ); endif; ?>
			</div>
		</section>

		<?php if ( $faq ) : ?>
		<section class="niv-section niv-section--alt"><div class="niv-container"><?php niv_render_faq( $faq ); ?></div></section>
		<?php endif; ?>

		<!-- קישורים פנימיים: שירות אב, אזור אב, סמוכים -->
		<section class="niv-section">
			<div class="niv-container niv-narrow">
				<h2>קישורים שימושיים</h2>
				<ul>
					<?php if ( $service ) : ?><li><a href="<?php echo esc_url( get_permalink( $service ) ); ?>"><?php echo esc_html( get_the_title( $service ) ); ?></a></li><?php endif; ?>
					<?php if ( $area ) : ?><li><a href="<?php echo esc_url( get_permalink( $area ) ); ?>">מנעולן ב<?php echo esc_html( get_the_title( $area ) ); ?></a></li><?php endif; ?>
					<?php
					if ( $links ) {
						foreach ( $links as $l ) {
							if ( ! empty( $l['link'] ) ) {
								printf( '<li><a href="%s">%s</a></li>', esc_url( is_array( $l['link'] ) ? $l['link']['url'] : $l['link'] ), esc_html( $l['label'] ?? '' ) );
							}
						}
					}
					?>
				</ul>
			</div>
		</section>

		<section class="niv-section niv-cta-strip">
			<div class="niv-container niv-narrow">
				<h2><?php echo esc_html( $h1 ); ?>?</h2>
				<div class="niv-btn-row">
					<?php niv_call_button( array( 'location' => 'sap-cta', 'text' => niv_has_phone() ? niv_phone_display() : 'חייגו עכשיו', 'class' => 'niv-btn--lg' ) ); ?>
					<?php niv_whatsapp_button( array( 'location' => 'sap-cta', 'class' => 'niv-btn--lg niv-btn--ghost-light' ) ); ?>
				</div>
			</div>
		</section>
	</main>

<?php endwhile; get_footer(); ?>
