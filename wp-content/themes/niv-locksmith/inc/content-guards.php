<?php
/**
 * שערי תוכן — מונעים עמודים דקים/ריקים מלעלות לאוויר.
 *
 * @package niv
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * service_area_page בלי unique_intro => נכפה draft בשמירה.
 * מונע doorway pages (docs/02 + 03).
 */
function niv_guard_service_area_page( $data, $postarr ) {
	if ( 'service_area_page' !== $data['post_type'] ) {
		return $data;
	}
	if ( 'publish' !== $data['post_status'] ) {
		return $data;
	}
	$post_id = isset( $postarr['ID'] ) ? $postarr['ID'] : 0;
	if ( ! $post_id || ! function_exists( 'get_field' ) ) {
		return $data;
	}

	$intro = get_field( 'unique_intro', $post_id );
	$words = str_word_count( wp_strip_all_tags( (string) $intro ) );

	// עברית: str_word_count לא מדויק, נשתמש בספירת רווחים גם.
	$he_words = count( preg_split( '/\s+/', trim( wp_strip_all_tags( (string) $intro ) ) ) );

	if ( empty( $intro ) || $he_words < 40 ) {
		$data['post_status'] = 'draft';
		set_transient( 'niv_guard_notice_' . $post_id, 'העמוד הוחזר לטיוטה: נדרש טקסט "אינטרו ייחודי" של 40+ מילים כדי למנוע תוכן דק.', 60 );
	}
	return $data;
}
add_filter( 'wp_insert_post_data', 'niv_guard_service_area_page', 10, 2 );

/**
 * הודעת admin אחרי הכפיית draft.
 */
function niv_guard_admin_notice() {
	global $post;
	if ( ! $post ) {
		return;
	}
	$msg = get_transient( 'niv_guard_notice_' . $post->ID );
	if ( $msg ) {
		delete_transient( 'niv_guard_notice_' . $post->ID );
		printf( '<div class="notice notice-warning"><p>%s</p></div>', esc_html( $msg ) );
	}
}
add_action( 'admin_notices', 'niv_guard_admin_notice' );
