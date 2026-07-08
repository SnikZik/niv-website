<?php
/**
 * ארכיון שירותים — גריד לפי קטגוריית שירות.
 *
 * @package niv
 */

get_header(); ?>
<main id="niv-main">
	<div class="niv-container"><?php niv_breadcrumbs(); ?></div>
	<section class="niv-section">
		<div class="niv-container">
			<div class="niv-section__head">
				<h1>שירותי מנעולן בירושלים</h1>
				<p>כל מה שניב מטפל בו — דלתות, צילינדרים, מנגנונים, כספות ומנעולים חכמים.</p>
			</div>

			<?php
			// קיבוץ לפי קטגוריה אם קיימת.
			$cats = get_terms( array( 'taxonomy' => 'service_category', 'hide_empty' => true ) );
			if ( $cats && ! is_wp_error( $cats ) ) :
				foreach ( $cats as $cat ) :
					$q = new WP_Query( array( 'post_type' => 'service', 'posts_per_page' => -1, 'tax_query' => array( array( 'taxonomy' => 'service_category', 'terms' => $cat->term_id ) ) ) );
					if ( $q->have_posts() ) : ?>
						<h2 style="margin-top:2rem"><?php echo esc_html( $cat->name ); ?></h2>
						<div class="niv-cards">
							<?php while ( $q->have_posts() ) : $q->the_post(); ?>
								<article class="niv-card">
									<div class="niv-card__icon"><?php echo niv_icon( 'lock' ); ?></div>
									<h3><a href="<?php the_permalink(); ?>" class="js-service-card" data-service="<?php echo esc_attr( get_the_title() ); ?>"><?php the_title(); ?></a></h3>
									<p><?php echo esc_html( get_field( 'short_desc' ) ); ?></p>
									<a class="niv-card__link" href="<?php the_permalink(); ?>">לפרטים ‹</a>
								</article>
							<?php endwhile; ?>
						</div>
					<?php endif; wp_reset_postdata();
				endforeach;
			else : ?>
				<div class="niv-cards">
					<?php while ( have_posts() ) : the_post(); ?>
						<article class="niv-card">
							<div class="niv-card__icon"><?php echo niv_icon( 'lock' ); ?></div>
							<h3><a href="<?php the_permalink(); ?>" class="js-service-card" data-service="<?php echo esc_attr( get_the_title() ); ?>"><?php the_title(); ?></a></h3>
							<p><?php echo esc_html( get_field( 'short_desc' ) ); ?></p>
							<a class="niv-card__link" href="<?php the_permalink(); ?>">לפרטים ‹</a>
						</article>
					<?php endwhile; ?>
				</div>
			<?php endif; ?>
		</div>
	</section>

	<section class="niv-section niv-cta-strip">
		<div class="niv-container niv-narrow">
			<h2>לא בטוחים איזה שירות צריך?</h2>
			<p>התקשרו ותארו מה קורה — נכוון אתכם.</p>
			<div class="niv-btn-row">
				<?php niv_call_button( array( 'location' => 'archive-service-cta', 'text' => niv_has_phone() ? niv_phone_display() : 'חייגו עכשיו', 'class' => 'niv-btn--lg' ) ); ?>
			</div>
		</div>
	</section>
</main>
<?php get_footer(); ?>
