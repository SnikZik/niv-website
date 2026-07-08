<?php
/**
 * רישום Custom Post Types + Taxonomies.
 * slugs בעברית. אחרי החלפת תמה — flush rewrite (ראה סוף הקובץ).
 *
 * @package niv
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function niv_register_cpts() {

	// --- שירותים ---
	register_post_type( 'service', array(
		'labels' => array(
			'name'          => __( 'שירותים', 'niv' ),
			'singular_name' => __( 'שירות', 'niv' ),
			'add_new_item'  => __( 'שירות חדש', 'niv' ),
			'edit_item'     => __( 'עריכת שירות', 'niv' ),
		),
		'public'       => true,
		'has_archive'  => 'שירותים',
		'menu_icon'    => 'dashicons-admin-tools',
		'menu_position'=> 20,
		'supports'     => array( 'title', 'editor', 'thumbnail', 'excerpt', 'revisions' ),
		'rewrite'      => array( 'slug' => 'שירותים', 'with_front' => false ),
		'show_in_rest' => true,
	) );

	// --- אזורי שירות ---
	register_post_type( 'service_area', array(
		'labels' => array(
			'name'          => __( 'אזורי שירות', 'niv' ),
			'singular_name' => __( 'אזור שירות', 'niv' ),
			'add_new_item'  => __( 'אזור חדש', 'niv' ),
		),
		'public'       => true,
		'has_archive'  => 'אזורי-שירות',
		'menu_icon'    => 'dashicons-location',
		'menu_position'=> 21,
		'supports'     => array( 'title', 'editor', 'thumbnail', 'excerpt', 'revisions' ),
		'rewrite'      => array( 'slug' => 'אזורי-שירות', 'with_front' => false ),
		'show_in_rest' => true,
	) );

	// --- שירות×אזור (פרוגרמטי) ---
	register_post_type( 'service_area_page', array(
		'labels' => array(
			'name'          => __( 'שירות × אזור', 'niv' ),
			'singular_name' => __( 'עמוד שירות×אזור', 'niv' ),
			'add_new_item'  => __( 'עמוד שירות×אזור חדש', 'niv' ),
		),
		'public'       => true,
		'has_archive'  => false, // הארכיון שלו = עמוד האזור.
		'menu_icon'    => 'dashicons-networking',
		'menu_position'=> 22,
		'supports'     => array( 'title', 'thumbnail', 'revisions' ),
		// slug נפרד מ-service_area כדי למנוע התנגשות rewrite (שניהם על 'אזורי-שירות' יצרו קונפליקט).
		// URL: /מנעולן/{שירות}-ב{אזור}/ ; עמוד האזור נשאר /אזורי-שירות/מנעולן-ב{אזור}/.
		'rewrite'      => array( 'slug' => 'מנעולן', 'with_front' => false ),
		'show_in_rest' => true,
	) );
}
add_action( 'init', 'niv_register_cpts', 5 );

function niv_register_taxonomies() {

	register_taxonomy( 'service_category', 'service', array(
		'labels' => array(
			'name'          => __( 'קטגוריות שירות', 'niv' ),
			'singular_name' => __( 'קטגוריית שירות', 'niv' ),
		),
		'public'            => true,
		'hierarchical'      => true,
		'show_admin_column' => true,
		'rewrite'           => array( 'slug' => 'קטגוריית-שירות', 'with_front' => false ),
		'show_in_rest'      => true,
	) );

	register_taxonomy( 'area_type', 'service_area', array(
		'labels' => array(
			'name'          => __( 'סוג אזור', 'niv' ),
			'singular_name' => __( 'סוג אזור', 'niv' ),
		),
		'public'            => false,
		'show_ui'           => true,
		'hierarchical'      => true,
		'show_admin_column' => true,
		'show_in_rest'      => true,
	) );
}
add_action( 'init', 'niv_register_taxonomies', 5 );

/**
 * flush rewrite rules פעם אחת אחרי הפעלת התמה (slugs עבריים דורשים זאת).
 */
function niv_flush_rewrites() {
	niv_register_cpts();
	niv_register_taxonomies();
	flush_rewrite_rules();
}
add_action( 'after_switch_theme', 'niv_flush_rewrites' );
