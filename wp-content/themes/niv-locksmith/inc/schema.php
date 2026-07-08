<?php
/**
 * JSON-LD schema. מקור אחד לכל טיפוס. בלי דירוג/ביקורות מזויפים.
 *
 * @package niv
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Locksmith (LocalBusiness) — בכל עמוד. נתונים מ-Business Settings.
 */
function niv_schema_locksmith() {
	$phone = niv_phone_e164();
	$data = array(
		'@context' => 'https://schema.org',
		'@type'    => 'Locksmith',
		'@id'      => home_url( '/#business' ),
		'name'     => niv_biz( 'biz_name', 'ניב המנעולן' ),
		'url'      => home_url( '/' ),
		'areaServed' => niv_biz( 'biz_area_text', 'ירושלים והסביבה' ),
		'address'  => array(
			'@type'           => 'PostalAddress',
			'addressLocality' => niv_biz( 'biz_city', 'ירושלים' ),
			'addressCountry'  => 'IL',
		),
	);

	if ( $phone ) {
		$data['telephone'] = $phone;
	}
	$email = niv_biz( 'biz_email' );
	if ( $email ) {
		$data['email'] = $email;
	}
	$logo = niv_biz( 'biz_logo' );
	if ( $logo && is_array( $logo ) ) {
		$data['image'] = $logo['url'];
		$data['logo']  = $logo['url'];
	}

	// שעות — רק אם הוגדרו. 24/7 רק אם אושר ב-ACF.
	$hours = niv_biz( 'biz_hours' );
	if ( ! empty( $hours ) && is_array( $hours ) ) {
		$spec = array();
		foreach ( $hours as $h ) {
			if ( ! empty( $h['is_24'] ) ) {
				$spec[] = array(
					'@type'     => 'OpeningHoursSpecification',
					'dayOfWeek' => array( 'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday' ),
					'opens'     => '00:00',
					'closes'    => '23:59',
				);
				break;
			}
		}
		if ( $spec ) {
			$data['openingHoursSpecification'] = $spec;
		}
	}

	// social — sameAs.
	$social = niv_biz( 'biz_social' );
	if ( ! empty( $social ) && is_array( $social ) ) {
		$data['sameAs'] = array_filter( wp_list_pluck( $social, 'url' ) );
	}

	niv_print_jsonld( $data );
}

/**
 * WebSite — בית בלבד.
 */
function niv_schema_website() {
	niv_print_jsonld( array(
		'@context' => 'https://schema.org',
		'@type'    => 'WebSite',
		'name'     => niv_biz( 'biz_name', 'ניב המנעולן' ),
		'url'      => home_url( '/' ),
		'inLanguage' => 'he-IL',
	) );
}

/**
 * Service — עמוד שירות / שירות×אזור.
 */
function niv_schema_service( $service_name, $area = '' ) {
	$data = array(
		'@context'    => 'https://schema.org',
		'@type'       => 'Service',
		'serviceType' => $service_name,
		'provider'    => array( '@id' => home_url( '/#business' ) ),
		'areaServed'  => $area ? $area : niv_biz( 'biz_area_text', 'ירושלים והסביבה' ),
		'name'        => get_the_title(),
	);
	niv_print_jsonld( $data );
}

/**
 * FAQPage — רק אם ה-FAQ מוצג בעמוד.
 */
function niv_schema_faq( $faqs ) {
	if ( empty( $faqs ) || ! is_array( $faqs ) ) {
		return;
	}
	$entities = array();
	foreach ( $faqs as $faq ) {
		if ( empty( $faq['q'] ) || empty( $faq['a'] ) ) { continue; }
		$entities[] = array(
			'@type'          => 'Question',
			'name'           => wp_strip_all_tags( $faq['q'] ),
			'acceptedAnswer' => array(
				'@type' => 'Answer',
				'text'  => wp_strip_all_tags( $faq['a'] ),
			),
		);
	}
	if ( ! $entities ) { return; }
	niv_print_jsonld( array(
		'@context'   => 'https://schema.org',
		'@type'      => 'FAQPage',
		'mainEntity' => $entities,
	) );
}

/**
 * BreadcrumbList — מקבל array של name/url.
 */
function niv_schema_breadcrumbs( $items ) {
	if ( empty( $items ) ) { return; }
	$list = array();
	foreach ( $items as $i => $item ) {
		$entry = array(
			'@type'    => 'ListItem',
			'position' => $i + 1,
			'name'     => $item['name'],
		);
		if ( ! empty( $item['url'] ) ) {
			$entry['item'] = $item['url'];
		}
		$list[] = $entry;
	}
	niv_print_jsonld( array(
		'@context'        => 'https://schema.org',
		'@type'           => 'BreadcrumbList',
		'itemListElement' => $list,
	) );
}

function niv_print_jsonld( $data ) {
	echo '<script type="application/ld+json">' . wp_json_encode( $data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
}

/**
 * הזרקה ל-head לפי סוג עמוד.
 */
function niv_output_schema() {
	niv_schema_locksmith();

	if ( is_front_page() ) {
		niv_schema_website();
	}

	if ( is_singular( 'service' ) ) {
		niv_schema_service( get_the_title() );
	} elseif ( is_singular( 'service_area_page' ) ) {
		$ctx = niv_page_context();
		niv_schema_service( $ctx['service'] ?: get_the_title(), $ctx['area'] );
	}

	// FAQ — אם לעמוד יש שדה faq.
	if ( is_singular() && function_exists( 'get_field' ) ) {
		$faqs = get_field( 'faq' );
		if ( ! empty( $faqs ) ) {
			niv_schema_faq( $faqs );
		}
	}
}
add_action( 'wp_head', 'niv_output_schema', 20 );
