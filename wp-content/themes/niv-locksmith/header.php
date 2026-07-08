<?php
/**
 * Header — לוגו + טלפון בולט + תפריט. עקרון מותג: טלפון בראש כל עמוד.
 *
 * @package niv
 */
?><!DOCTYPE html>
<html <?php language_attributes(); ?> dir="rtl">
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<a class="niv-skip-link" href="#niv-main"><?php esc_html_e( 'דלג לתוכן', 'niv' ); ?></a>

<header class="niv-header" role="banner">
	<div class="niv-header__inner niv-container">

		<a class="niv-logo" href="<?php echo esc_url( home_url( '/' ) ); ?>" aria-label="<?php echo esc_attr( niv_biz( 'biz_name', 'ניב המנעולן' ) ); ?> — לעמוד הבית">
			<?php
			$logo = niv_biz( 'biz_logo' );
			if ( $logo && is_array( $logo ) ) :
				printf( '<img src="%s" alt="%s" width="180" height="56" />', esc_url( $logo['url'] ), esc_attr( niv_biz( 'biz_name', 'ניב המנעולן' ) ) );
			else :
				// placeholder טקסטואלי עד שיגיע קובץ הלוגו (NEEDS_CLIENT_INPUT).
				echo '<span class="niv-logo__text">ניב <strong>המנעולן</strong></span>';
			endif;
			?>
		</a>

		<nav class="niv-nav" aria-label="<?php esc_attr_e( 'תפריט ראשי', 'niv' ); ?>">
			<button class="niv-nav__toggle" aria-expanded="false" aria-controls="niv-primary-menu" aria-label="<?php esc_attr_e( 'פתיחת תפריט', 'niv' ); ?>">
				<span></span><span></span><span></span>
			</button>
			<?php
			wp_nav_menu( array(
				'theme_location' => 'primary',
				'menu_id'        => 'niv-primary-menu',
				'menu_class'     => 'niv-nav__menu',
				'container'      => false,
				'fallback_cb'    => 'niv_default_menu',
				'depth'          => 2,
			) );
			?>
		</nav>

		<div class="niv-header__cta">
			<?php if ( niv_has_phone() ) : ?>
				<span class="niv-header__phone-label"><?php esc_html_e( 'לשירות מיידי', 'niv' ); ?></span>
			<?php endif; ?>
			<?php niv_call_button( array( 'location' => 'header', 'text' => niv_has_phone() ? niv_phone_display() : 'חייגו עכשיו', 'class' => 'niv-btn--sm' ) ); ?>
		</div>

	</div>
</header>

<?php
/**
 * תפריט ברירת מחדל אם לא הוגדר בממשק.
 */
function niv_default_menu() {
	echo '<ul id="niv-primary-menu" class="niv-nav__menu">';
	echo '<li><a href="' . esc_url( home_url( '/' ) ) . '">בית</a></li>';
	$svc = get_post_type_archive_link( 'service' );
	$area = get_post_type_archive_link( 'service_area' );
	if ( $svc )  { echo '<li><a href="' . esc_url( $svc ) . '">שירותים</a></li>'; }
	if ( $area ) { echo '<li><a href="' . esc_url( $area ) . '">אזורי שירות</a></li>'; }
	echo '<li><a href="' . esc_url( home_url( '/מדריכים/' ) ) . '">מדריכים</a></li>';
	echo '<li><a href="' . esc_url( home_url( '/יצירת-קשר/' ) ) . '">צור קשר</a></li>';
	echo '</ul>';
}
