<?php
/**
 * עמוד שירות בודד. מבנה לפי docs/08.
 *
 * @package niv
 */

get_header();

while ( have_posts() ) : the_post();
	$hero_title = get_field( 'hero_title' ) ?: get_the_title();
	$hero_sub   = get_field( 'hero_subtitle' );
	$problem    = get_field( 'problem_desc' );
	$solution   = get_field( 'solution_desc' );
	$scenarios  = get_field( 'scenarios' );
	$factors    = get_field( 'price_factors' );
	$faq        = get_field( 'faq' );
	$related_s  = get_field( 'related_services' );
	$related_a  = get_field( 'related_areas' );
	?>

	<main id="niv-main">
		<div class="niv-container"><?php niv_breadcrumbs(); ?></div>

		<!-- הירו -->
		<section class="niv-hero">
			<?php if ( has_post_thumbnail() ) : ?>
				<div class="niv-hero__media"><?php the_post_thumbnail( 'niv_hero', array( 'alt' => esc_attr( $hero_title ), 'loading' => 'eager', 'fetchpriority' => 'high' ) ); ?></div>
			<?php endif; ?>
			<div class="niv-container niv-hero__inner">
				<div class="niv-hero__content">
					<h1><?php echo esc_html( $hero_title ); ?></h1>
					<?php if ( $hero_sub ) : ?><p class="niv-hero__sub"><?php echo esc_html( $hero_sub ); ?></p><?php endif; ?>
					<div class="niv-btn-row">
						<?php niv_call_button( array( 'location' => 'service-hero', 'text' => 'חייגו עכשיו', 'class' => 'niv-btn--lg' ) ); ?>
						<?php niv_whatsapp_button( array( 'location' => 'service-hero', 'class' => 'niv-btn--lg' ) ); ?>
					</div>
				</div>
			</div>
		</section>

		<!-- גוף השירות -->
		<section class="niv-section">
			<div class="niv-container niv-prose">
				<?php if ( $problem ) : ?>
					<h2>מתי קוראים לניב</h2>
					<?php echo wp_kses_post( $problem ); ?>
				<?php endif; ?>

				<?php if ( $solution ) : ?>
					<h2>איך מטפלים בזה</h2>
					<?php echo wp_kses_post( $solution ); ?>
				<?php endif; ?>

				<?php if ( ! $problem && ! $solution ) : the_content(); endif; ?>

				<?php if ( $scenarios ) : ?>
					<h2>מקרים נפוצים</h2>
					<ul>
						<?php foreach ( $scenarios as $sc ) : ?>
							<li><?php echo esc_html( is_array( $sc ) ? ( $sc['scenario'] ?? '' ) : $sc ); ?></li>
						<?php endforeach; ?>
					</ul>
				<?php endif; ?>

				<?php if ( $factors ) : ?>
					<h2>מה משפיע על המחיר</h2>
					<ul class="niv-factors">
						<?php foreach ( $factors as $f ) : ?>
							<li><span><b><?php echo esc_html( $f['factor'] ?? '' ); ?></b> — <?php echo esc_html( $f['impact'] ?? '' ); ?></span></li>
						<?php endforeach; ?>
					</ul>
					<p class="niv-muted">המחיר הסופי נקבע לפי סוג הדלת והתקלה בפועל. תמיד נאמר לכם מחיר או הערכה לפני שמתחילים.</p>
				<?php endif; ?>
			</div>
		</section>

		<!-- CTA אמצע -->
		<section class="niv-section niv-cta-strip">
			<div class="niv-container niv-narrow">
				<h2>צריכים <?php echo esc_html( get_the_title() ); ?>?</h2>
				<div class="niv-btn-row">
					<?php niv_call_button( array( 'location' => 'service-mid', 'text' => niv_has_phone() ? niv_phone_display() : 'חייגו עכשיו', 'class' => 'niv-btn--lg' ) ); ?>
					<?php niv_whatsapp_button( array( 'location' => 'service-mid', 'class' => 'niv-btn--lg niv-btn--ghost-light' ) ); ?>
				</div>
			</div>
		</section>

		<!-- FAQ -->
		<?php if ( $faq ) : ?>
		<section class="niv-section">
			<div class="niv-container"><?php niv_render_faq( $faq ); ?></div>
		</section>
		<?php endif; ?>

		<!-- שירותים + אזורים קשורים -->
		<section class="niv-section niv-section--alt">
			<div class="niv-container">
				<?php if ( $related_s ) : ?>
					<h2>שירותים נוספים</h2>
					<div class="niv-cards">
						<?php foreach ( $related_s as $rs ) : ?>
							<article class="niv-card">
								<h3><a href="<?php echo esc_url( get_permalink( $rs ) ); ?>"><?php echo esc_html( get_the_title( $rs ) ); ?></a></h3>
								<p><?php echo esc_html( get_field( 'short_desc', is_object( $rs ) ? $rs->ID : $rs ) ); ?></p>
							</article>
						<?php endforeach; ?>
					</div>
				<?php endif; ?>

				<?php if ( $related_a ) : ?>
					<h2 style="margin-top:2rem">אזורי שירות</h2>
					<div class="niv-areas">
						<?php foreach ( $related_a as $ra ) : ?>
							<a class="niv-area-chip js-area-card" data-area="<?php echo esc_attr( get_the_title( $ra ) ); ?>" href="<?php echo esc_url( get_permalink( $ra ) ); ?>"><?php echo niv_icon( 'home' ); ?><?php echo esc_html( get_the_title( $ra ) ); ?></a>
						<?php endforeach; ?>
					</div>
				<?php endif; ?>
			</div>
		</section>

	</main>

<?php endwhile; get_footer(); ?>
