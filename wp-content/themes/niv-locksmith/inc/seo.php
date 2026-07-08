<?php
/**
 * SEO meta — title/description/OG לפי תבניות docs/03.
 * אם Yoast/RankMath פעיל — נותנים לו לנהל ומדלגים (מונע כפילות).
 *
 * @package niv
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * האם מנוע SEO חיצוני מנהל את ה-head.
 */
function niv_seo_plugin_active() {
	return defined( 'WPSEO_VERSION' ) || class_exists( 'RankMath' );
}

/**
 * meta description לפי תבנית + fallback חכם.
 */
function niv_meta_description() {
	// ACF מפורש קודם.
	if ( is_singular() && function_exists( 'get_field' ) ) {
		$m = get_field( 'meta_description' );
		if ( $m ) { return $m; }
	}

	$city = niv_biz( 'biz_city', 'ירושלים' );

	if ( is_front_page() ) {
		return 'צריכים מנעולן לדלתות בירושלים? ניב המנעולן מספק מענה לדלתות, צילינדרים, מנגנונים ותקלות נעילה באזור ירושלים. התקשרו לקבלת מענה מהיר.';
	}
	if ( is_singular( 'service' ) ) {
		return sprintf( 'צריכים %s? ניב המנעולן מספק שירות מקצועי לדלתות, צילינדרים ומנגנונים עם הסבר ברור לפני העבודה. חייגו עכשיו.', get_the_title() );
	}
	if ( is_singular( 'service_area' ) ) {
		$area = function_exists( 'get_field' ) ? ( get_field( 'area_name' ) ?: get_the_title() ) : get_the_title();
		return sprintf( 'מחפשים מנעולן ב%s? ניב המנעולן נותן מענה לדלתות, צילינדרים ותקלות נעילה באזור %s והסביבה. התקשרו עכשיו.', $area, $area );
	}
	if ( is_singular( 'service_area_page' ) ) {
		$ctx = niv_page_context();
		return sprintf( 'צריכים %s ב%s? ניב המנעולן מספק מענה מהיר וברור לתקלות דלתות ומנעולים באזור %s. חייגו לקבלת פרטים.', $ctx['service'], $ctx['area'], $ctx['area'] );
	}
	if ( is_singular( 'post' ) ) {
		return wp_trim_words( wp_strip_all_tags( get_the_excerpt() ), 26 );
	}
	return get_bloginfo( 'description' );
}

/**
 * title לפי תבנית (רק אם אין מנוע SEO ואין ACF seo_title).
 */
function niv_filter_title( $title ) {
	if ( is_singular() && function_exists( 'get_field' ) ) {
		$t = get_field( 'seo_title' );
		if ( $t ) { return $t; }
	}
	return $title;
}

/**
 * הזרקת meta ל-head (רק אם אין מנוע SEO חיצוני).
 */
function niv_output_meta() {
	if ( niv_seo_plugin_active() ) {
		return;
	}

	$desc = niv_meta_description();
	$og_img = '';
	if ( is_singular() && has_post_thumbnail() ) {
		$og_img = get_the_post_thumbnail_url( null, 'niv_hero' );
	}
	if ( ! $og_img ) {
		$fallback = niv_biz( 'biz_og' );
		$og_img = ( $fallback && is_array( $fallback ) ) ? $fallback['url'] : '';
	}

	echo '<meta name="description" content="' . esc_attr( $desc ) . '">' . "\n";
	echo '<meta property="og:locale" content="he_IL">' . "\n";
	echo '<meta property="og:type" content="' . ( is_singular( 'post' ) ? 'article' : 'website' ) . '">' . "\n";
	echo '<meta property="og:title" content="' . esc_attr( wp_get_document_title() ) . '">' . "\n";
	echo '<meta property="og:description" content="' . esc_attr( $desc ) . '">' . "\n";
	echo '<meta property="og:url" content="' . esc_url( is_singular() ? get_permalink() : home_url( add_query_arg( null, null ) ) ) . '">' . "\n";
	if ( $og_img ) {
		echo '<meta property="og:image" content="' . esc_url( $og_img ) . '">' . "\n";
		echo '<meta name="twitter:card" content="summary_large_image">' . "\n";
	}
	// canonical (ACF override).
	$canonical = is_singular() && function_exists( 'get_field' ) ? get_field( 'canonical_url' ) : '';
	if ( ! $canonical && is_singular() ) {
		$canonical = get_permalink();
	}
	if ( $canonical ) {
		echo '<link rel="canonical" href="' . esc_url( $canonical ) . '">' . "\n";
	}
}
add_action( 'wp_head', 'niv_output_meta', 1 );
add_filter( 'pre_get_document_title', 'niv_filter_title', 20 );

/**
 * noindex לעמודי שירות×אזור שלא סומנו index (שער thin-content).
 */
function niv_maybe_noindex() {
	if ( niv_seo_plugin_active() ) {
		return; // המנוע מטפל לפי ACF robots.
	}
	if ( is_singular( 'service_area_page' ) && function_exists( 'get_field' ) ) {
		$status = get_field( 'index_status' );
		if ( 'index' !== $status ) {
			echo '<meta name="robots" content="noindex,follow">' . "\n";
		}
	}
}
add_action( 'wp_head', 'niv_maybe_noindex', 1 );
