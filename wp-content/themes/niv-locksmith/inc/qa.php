<?php
/**
 * QA scanner — עמוד admin שסורק בעיות SEO/תוכן לפני launch.
 * Tools → QA ניב.
 *
 * @package niv
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function niv_qa_menu() {
	add_management_page( 'QA ניב', 'QA ניב', 'manage_options', 'niv-qa', 'niv_qa_page' );
}
add_action( 'admin_menu', 'niv_qa_menu' );

function niv_qa_page() {
	echo '<div class="wrap"><h1>QA ניב המנעולן</h1>';

	$types = array( 'page', 'service', 'service_area', 'service_area_page', 'post' );
	$posts = get_posts( array(
		'post_type'   => $types,
		'post_status' => 'publish',
		'numberposts' => -1,
	) );

	$titles = array();
	$metas  = array();
	$issues = array();

	foreach ( $posts as $p ) {
		$seo_title = get_field( 'seo_title', $p->ID );
		$meta = get_field( 'meta_description', $p->ID );
		$link = get_edit_post_link( $p->ID );
		$label = get_the_title( $p ) . " (#{$p->ID})";

		// כפילות title.
		if ( $seo_title ) {
			$titles[ $seo_title ][] = $label;
			$len = mb_strlen( $seo_title );
			if ( $len < 45 || $len > 65 ) {
				$issues[] = "אורך SEO title חריג ({$len} תווים): {$label}";
			}
		}
		// כפילות meta.
		if ( $meta ) {
			$metas[ $meta ][] = $label;
			$len = mb_strlen( $meta );
			if ( $len < 120 || $len > 155 ) {
				$issues[] = "אורך meta description חריג ({$len} תווים): {$label}";
			}
		}
		// H1 — בדיקת content לא ריק.
		if ( in_array( $p->post_type, array( 'service', 'service_area', 'service_area_page' ), true ) && ! trim( wp_strip_all_tags( $p->post_content ) ) && ! get_field( 'unique_intro', $p->ID ) && ! get_field( 'solution_desc', $p->ID ) && ! get_field( 'local_intro', $p->ID ) ) {
			$issues[] = "תוכן ריק (סיכון thin): {$label}";
		}
		// תמונה ראשית ללא alt.
		$thumb_id = get_post_thumbnail_id( $p->ID );
		if ( $thumb_id && ! get_post_meta( $thumb_id, '_wp_attachment_image_alt', true ) ) {
			$issues[] = "תמונה ראשית ללא alt: {$label}";
		}
	}

	foreach ( $titles as $t => $where ) {
		if ( count( $where ) > 1 ) {
			$issues[] = 'SEO title כפול (' . esc_html( $t ) . '): ' . implode( ', ', $where );
		}
	}
	foreach ( $metas as $m => $where ) {
		if ( count( $where ) > 1 ) {
			$issues[] = 'meta description כפול: ' . implode( ', ', $where );
		}
	}

	if ( empty( $issues ) ) {
		echo '<div class="notice notice-success inline"><p>✓ לא נמצאו בעיות QA.</p></div>';
	} else {
		echo '<div class="notice notice-warning inline"><p><strong>' . count( $issues ) . ' בעיות:</strong></p><ul style="list-style:disc;padding-inline-start:2em">';
		foreach ( $issues as $iss ) {
			echo '<li>' . esc_html( $iss ) . '</li>';
		}
		echo '</ul></div>';
	}
	echo '</div>';
}
