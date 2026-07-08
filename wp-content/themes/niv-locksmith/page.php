<?php
/**
 * עמוד רגיל. אם קיים ACF flexible `sections` — טוען layouts; אחרת the_content.
 *
 * @package niv
 */

get_header();

while ( have_posts() ) : the_post(); ?>
	<main id="niv-main">
		<div class="niv-container"><?php niv_breadcrumbs(); ?></div>

		<?php if ( function_exists( 'have_rows' ) && have_rows( 'sections' ) ) : ?>
			<?php while ( have_rows( 'sections' ) ) : the_row();
				$layout = get_row_layout();
				// טוען template-parts/flexible/{layout}.php אם קיים.
				get_template_part( 'template-parts/flexible/' . $layout );
			endwhile; ?>
		<?php else : ?>
			<article class="niv-section">
				<div class="niv-container niv-prose">
					<h1><?php the_title(); ?></h1>
					<?php the_content(); ?>
				</div>
			</article>
		<?php endif; ?>

		<section class="niv-section niv-cta-strip">
			<div class="niv-container niv-narrow">
				<h2>צריכים מנעולן בירושלים?</h2>
				<div class="niv-btn-row">
					<?php niv_call_button( array( 'location' => 'page-cta', 'text' => niv_has_phone() ? niv_phone_display() : 'חייגו עכשיו', 'class' => 'niv-btn--lg' ) ); ?>
					<?php niv_whatsapp_button( array( 'location' => 'page-cta', 'class' => 'niv-btn--lg niv-btn--ghost-light' ) ); ?>
				</div>
			</div>
		</section>
	</main>
<?php endwhile; get_footer(); ?>
