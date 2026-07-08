<?php
/**
 * Template tags — עוזרים לשימוש חוזר: CTA, טלפון, פירורי לחם, הקשר עמוד.
 *
 * @package niv
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * שליפת הגדרת עסק מ-ACF options, עם fallback.
 */
function niv_biz( $key, $default = '' ) {
	if ( function_exists( 'get_field' ) ) {
		$val = get_field( $key, 'option' );
		if ( ! empty( $val ) ) {
			return $val;
		}
	}
	return $default;
}

/**
 * טלפון תצוגה (למשל 050-000-0000). placeholder אם חסר.
 */
function niv_phone_display() {
	return niv_biz( 'biz_phone_display', 'NEEDS_CLIENT_INPUT' );
}

/**
 * טלפון E.164 ל-tel: (+9725XXXXXXXX). ריק => כפתור מושבת.
 */
function niv_phone_e164() {
	return niv_biz( 'biz_phone_e164', '' );
}

function niv_whatsapp_e164() {
	return niv_biz( 'biz_wa', niv_phone_e164() );
}

/**
 * האם פרטי הקשר מוכנים (משפיע על השבתת CTA).
 */
function niv_has_phone() {
	return (bool) niv_phone_e164();
}

/**
 * הקשר העמוד הנוכחי — service / area — להזרקה ל-data attributes (tracking).
 * מחזיר array( 'service' => '', 'area' => '' ).
 */
function niv_page_context() {
	$ctx = array( 'service' => '', 'area' => '' );

	if ( is_singular( 'service' ) ) {
		$ctx['service'] = get_the_title();
	} elseif ( is_singular( 'service_area' ) ) {
		$ctx['area'] = get_the_title();
	} elseif ( is_singular( 'service_area_page' ) ) {
		$svc = function_exists( 'get_field' ) ? get_field( 'service_ref' ) : null;
		$area = function_exists( 'get_field' ) ? get_field( 'area_ref' ) : null;
		$ctx['service'] = $svc ? get_the_title( $svc ) : '';
		$ctx['area']    = $area ? get_the_title( $area ) : '';
	}
	return $ctx;
}

/**
 * כפתור חיוג. עקרון מותג: אדום, בולט, tel:.
 *
 * @param array $args location (data-cta-location), text, class, context (service/area).
 */
function niv_call_button( $args = array() ) {
	$ctx = niv_page_context();
	$args = wp_parse_args( $args, array(
		'location' => 'section',
		'text'     => niv_biz( 'biz_cta_primary', 'חייגו עכשיו' ),
		'class'    => '',
		'service'  => $ctx['service'],
		'area'     => $ctx['area'],
	) );

	$tel = niv_phone_e164();
	$disabled = $tel ? '' : ' niv-btn--disabled';
	$href = $tel ? 'tel:' . esc_attr( $tel ) : '#';

	printf(
		'<a class="niv-btn niv-btn--call js-call-click%1$s %2$s" href="%3$s" data-cta-location="%4$s" data-service="%5$s" data-area="%6$s" data-phone="%7$s" aria-label="%8$s">
			<span class="niv-btn__icon" aria-hidden="true">%9$s</span>%10$s</a>',
		esc_attr( $disabled ),
		esc_attr( $args['class'] ),
		esc_attr( $href ),
		esc_attr( $args['location'] ),
		esc_attr( $args['service'] ),
		esc_attr( $args['area'] ),
		esc_attr( $tel ),
		esc_attr__( 'חייגו לניב המנעולן', 'niv' ),
		niv_icon( 'phone' ),
		esc_html( $args['text'] )
	);
}

/**
 * כפתור WhatsApp.
 */
function niv_whatsapp_button( $args = array() ) {
	$ctx = niv_page_context();
	$args = wp_parse_args( $args, array(
		'location' => 'section',
		'text'     => niv_biz( 'biz_cta_secondary', 'שלחו WhatsApp' ),
		'class'    => '',
		'service'  => $ctx['service'],
		'area'     => $ctx['area'],
	) );

	$wa = preg_replace( '/\D/', '', niv_whatsapp_e164() );
	if ( ! $wa ) {
		return;
	}
	$msg = rawurlencode( 'שלום ניב, צריך/ה מנעולן' . ( $ctx['area'] ? ' ב' . $ctx['area'] : ' בירושלים' ) );
	$href = "https://wa.me/{$wa}?text={$msg}";

	printf(
		'<a class="niv-btn niv-btn--wa js-whatsapp-click %1$s" href="%2$s" target="_blank" rel="noopener" data-cta-location="%3$s" data-service="%4$s" data-area="%5$s" aria-label="%6$s">
			<span class="niv-btn__icon" aria-hidden="true">%7$s</span>%8$s</a>',
		esc_attr( $args['class'] ),
		esc_url( $href ),
		esc_attr( $args['location'] ),
		esc_attr( $args['service'] ),
		esc_attr( $args['area'] ),
		esc_attr__( 'שליחת הודעת וואטסאפ לניב', 'niv' ),
		niv_icon( 'whatsapp' ),
		esc_html( $args['text'] )
	);
}

/**
 * אייקוני קו (סגנון מותג: outline, בלי מילוי, currentColor).
 */
function niv_icon( $name ) {
	$icons = array(
		'phone'    => '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.3 1.8.6 2.6a2 2 0 0 1-.5 2.1L8 9.6a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.5c.8.3 1.7.5 2.6.6a2 2 0 0 1 1.7 2Z"/></svg>',
		'whatsapp' => '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.4 8.4 0 0 1-12.3 7.5L3 21l2-5.6A8.4 8.4 0 1 1 21 11.5Z"/></svg>',
		'lock'     => '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>',
		'key'      => '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="7.5" cy="15.5" r="4.5"/><path d="M10.5 12.5 21 2m-4 3 2 2m-4 0 2 2"/></svg>',
		'clock'    => '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
		'home'     => '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/></svg>',
		'shield'   => '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/></svg>',
	);
	return isset( $icons[ $name ] ) ? $icons[ $name ] : '';
}

/**
 * פירורי לחם — סמנטי + BreadcrumbList schema מוזרק ב-inc/schema.php.
 */
function niv_breadcrumbs() {
	if ( is_front_page() ) {
		return;
	}
	$items = array( array( 'name' => 'בית', 'url' => home_url( '/' ) ) );

	if ( is_singular( 'service' ) ) {
		$items[] = array( 'name' => 'שירותים', 'url' => get_post_type_archive_link( 'service' ) );
		$items[] = array( 'name' => get_the_title(), 'url' => '' );
	} elseif ( is_singular( 'service_area' ) ) {
		$items[] = array( 'name' => 'אזורי שירות', 'url' => get_post_type_archive_link( 'service_area' ) );
		$items[] = array( 'name' => get_the_title(), 'url' => '' );
	} elseif ( is_singular( 'service_area_page' ) ) {
		$items[] = array( 'name' => 'אזורי שירות', 'url' => get_post_type_archive_link( 'service_area' ) );
		$area = function_exists( 'get_field' ) ? get_field( 'area_ref' ) : null;
		if ( $area ) {
			$items[] = array( 'name' => get_the_title( $area ), 'url' => get_permalink( $area ) );
		}
		$items[] = array( 'name' => get_the_title(), 'url' => '' );
	} elseif ( is_singular( 'post' ) ) {
		$items[] = array( 'name' => 'מדריכים', 'url' => get_permalink( get_option( 'page_for_posts' ) ) );
		$items[] = array( 'name' => get_the_title(), 'url' => '' );
	} elseif ( is_page() ) {
		$items[] = array( 'name' => get_the_title(), 'url' => '' );
	}

	echo '<nav class="niv-breadcrumbs" aria-label="' . esc_attr__( 'פירורי לחם', 'niv' ) . '"><ol>';
	$last = count( $items ) - 1;
	foreach ( $items as $i => $item ) {
		if ( $i === $last || empty( $item['url'] ) ) {
			echo '<li aria-current="page">' . esc_html( $item['name'] ) . '</li>';
		} else {
			echo '<li><a href="' . esc_url( $item['url'] ) . '">' . esc_html( $item['name'] ) . '</a></li>';
		}
	}
	echo '</ol></nav>';
}

/**
 * FAQ אקורדיון נגיש. מקבל repeater של q/a.
 */
function niv_render_faq( $faqs, $heading = 'שאלות נפוצות' ) {
	if ( empty( $faqs ) || ! is_array( $faqs ) ) {
		return;
	}
	echo '<section class="niv-faq" aria-labelledby="niv-faq-title">';
	echo '<h2 id="niv-faq-title">' . esc_html( $heading ) . '</h2>';
	echo '<div class="niv-faq__list">';
	foreach ( $faqs as $i => $faq ) {
		$q = isset( $faq['q'] ) ? $faq['q'] : '';
		$a = isset( $faq['a'] ) ? $faq['a'] : '';
		if ( ! $q ) { continue; }
		$id = 'faq-' . $i;
		printf(
			'<div class="niv-faq__item">
				<h3 class="niv-faq__q"><button type="button" class="niv-faq__btn" aria-expanded="false" aria-controls="%1$s-a" id="%1$s-q">%2$s<span class="niv-faq__chevron" aria-hidden="true"></span></button></h3>
				<div class="niv-faq__a" id="%1$s-a" role="region" aria-labelledby="%1$s-q" hidden>%3$s</div>
			</div>',
			esc_attr( $id ),
			esc_html( $q ),
			wp_kses_post( wpautop( $a ) )
		);
	}
	echo '</div></section>';
}
