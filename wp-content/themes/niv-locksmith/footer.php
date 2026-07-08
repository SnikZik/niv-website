<?php
/**
 * Footer — קישורים פנימיים (שירותים/אזורים/מידע) + NAP + CTA דביק בנייד.
 *
 * @package niv
 */
?>

<footer class="niv-footer" role="contentinfo">
	<div class="niv-container niv-footer__grid">

		<div class="niv-footer__col niv-footer__brand">
			<span class="niv-logo__text niv-logo__text--footer">ניב <strong>המנעולן</strong></span>
			<p><?php echo esc_html( niv_biz( 'biz_area_text', 'מנעולן לדלתות בירושלים והסביבה' ) ); ?></p>
			<?php niv_call_button( array( 'location' => 'footer', 'text' => niv_has_phone() ? niv_phone_display() : 'חייגו עכשיו' ) ); ?>
		</div>

		<div class="niv-footer__col">
			<h2 class="niv-footer__title">שירותים</h2>
			<?php niv_footer_menu( 'footer_services', 'service' ); ?>
		</div>

		<div class="niv-footer__col">
			<h2 class="niv-footer__title">אזורי שירות</h2>
			<?php niv_footer_menu( 'footer_areas', 'service_area' ); ?>
		</div>

		<div class="niv-footer__col">
			<h2 class="niv-footer__title">מידע</h2>
			<ul class="niv-footer__list">
				<li><a href="<?php echo esc_url( home_url( '/אודות/' ) ); ?>">אודות ניב</a></li>
				<li><a href="<?php echo esc_url( home_url( '/יצירת-קשר/' ) ); ?>">יצירת קשר</a></li>
				<li><a href="<?php echo esc_url( home_url( '/מדריכים/' ) ); ?>">מדריכים</a></li>
				<li><a href="<?php echo esc_url( home_url( '/הצהרת-נגישות/' ) ); ?>">הצהרת נגישות</a></li>
				<li><a href="<?php echo esc_url( home_url( '/מדיניות-פרטיות/' ) ); ?>">מדיניות פרטיות</a></li>
			</ul>
		</div>

	</div>

	<div class="niv-footer__bottom niv-container">
		<p>&copy; <?php echo esc_html( wp_date( 'Y' ) ); ?> <?php echo esc_html( niv_biz( 'biz_name', 'ניב המנעולן' ) ); ?>. כל הזכויות שמורות.</p>
	</div>
</footer>

<?php get_template_part( 'template-parts/sticky-cta' ); ?>

<?php wp_footer(); ?>
</body>
</html>

<?php
/**
 * תפריט פוטר — נופל אוטומטית לרשימת CPT אם לא הוגדר בממשק.
 */
function niv_footer_menu( $location, $post_type ) {
	if ( has_nav_menu( $location ) ) {
		wp_nav_menu( array(
			'theme_location' => $location,
			'menu_class'     => 'niv-footer__list',
			'container'      => false,
			'depth'          => 1,
		) );
		return;
	}
	$items = get_posts( array( 'post_type' => $post_type, 'numberposts' => 8, 'post_status' => 'publish', 'orderby' => 'menu_order title', 'order' => 'ASC' ) );
	if ( ! $items ) {
		echo '<p class="niv-muted">בקרוב</p>';
		return;
	}
	echo '<ul class="niv-footer__list">';
	foreach ( $items as $item ) {
		printf( '<li><a href="%s">%s</a></li>', esc_url( get_permalink( $item ) ), esc_html( get_the_title( $item ) ) );
	}
	echo '</ul>';
}
