<?php
/**
 * fallback + ארכיון מדריכים.
 *
 * @package niv
 */

get_header(); ?>
<main id="niv-main">
	<section class="niv-section">
		<div class="niv-container">
			<div class="niv-section__head">
				<h1><?php echo is_home() ? 'מדריכי מנעולנות' : esc_html( get_the_archive_title() ); ?></h1>
				<?php if ( is_home() ) : ?><p>טיפים והסברים על דלתות, צילינדרים ומנעולים — ממנעולן שעובד בשטח בירושלים.</p><?php endif; ?>
			</div>

			<?php if ( have_posts() ) : ?>
				<div class="niv-cards">
					<?php while ( have_posts() ) : the_post(); ?>
						<article class="niv-card">
							<?php if ( has_post_thumbnail() ) : ?>
								<a href="<?php the_permalink(); ?>" tabindex="-1" aria-hidden="true"><?php the_post_thumbnail( 'niv_card', array( 'style' => 'border-radius:var(--niv-radius);margin-bottom:1rem' ) ); ?></a>
							<?php endif; ?>
							<h2 style="font-size:1.25rem"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
							<p><?php echo esc_html( wp_trim_words( get_the_excerpt(), 22 ) ); ?></p>
							<a class="niv-card__link" href="<?php the_permalink(); ?>">לקריאה ‹</a>
						</article>
					<?php endwhile; ?>
				</div>
				<div style="margin-top:2rem;text-align:center"><?php the_posts_pagination( array( 'mid_size' => 1 ) ); ?></div>
			<?php else : ?>
				<p class="niv-muted">אין עדיין מדריכים. בקרוב.</p>
			<?php endif; ?>
		</div>
	</section>
</main>
<?php get_footer(); ?>
