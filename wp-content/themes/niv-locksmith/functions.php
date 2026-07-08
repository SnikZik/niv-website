<?php
/**
 * ניב המנעולן — bootstrap התמה
 *
 * @package niv
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'NIV_VERSION', '0.1.0' );
define( 'NIV_DIR', get_template_directory() );
define( 'NIV_URI', get_template_directory_uri() );

/**
 * תמיכות ליבה של התמה.
 */
function niv_setup() {
	load_theme_textdomain( 'niv', NIV_DIR . '/languages' );

	add_theme_support( 'title-tag' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'automatic-feed-links' );
	add_theme_support( 'html5', array( 'search-form', 'gallery', 'caption', 'style', 'script', 'navigation-widgets' ) );
	add_theme_support( 'responsive-embeds' );

	register_nav_menus( array(
		'primary' => __( 'תפריט ראשי', 'niv' ),
		'footer_services' => __( 'פוטר — שירותים', 'niv' ),
		'footer_areas'    => __( 'פוטר — אזורים', 'niv' ),
		'footer_legal'    => __( 'פוטר — מידע', 'niv' ),
	) );

	// גדלי תמונה מותאמים (WebP מטופל בהעלאה/CDN).
	add_image_size( 'niv_hero', 1600, 900, true );
	add_image_size( 'niv_card', 640, 420, true );
}
add_action( 'after_setup_theme', 'niv_setup' );

/**
 * טעינת נכסים. פונטים מקומיים מומלצים (self-host) — ראה assets/fonts.
 * כברירת מחדל טוענים מ-Google Fonts עם preconnect.
 */
function niv_assets() {
	// Google Fonts: Frank Ruhl Libre (500,700,900) + Assistant (400,600,700,800).
	wp_enqueue_style(
		'niv-fonts',
		'https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&family=Frank+Ruhl+Libre:wght@500;700;900&display=swap',
		array(),
		null
	);

	wp_enqueue_style( 'niv-tokens', NIV_URI . '/assets/css/tokens.css', array(), NIV_VERSION );
	wp_enqueue_style( 'niv-main', NIV_URI . '/assets/css/main.css', array( 'niv-tokens' ), NIV_VERSION );

	wp_enqueue_script( 'niv-main', NIV_URI . '/assets/js/main.js', array(), NIV_VERSION, true );
	wp_enqueue_script( 'niv-tracking', NIV_URI . '/assets/js/tracking.js', array(), NIV_VERSION, true );
}
add_action( 'wp_enqueue_scripts', 'niv_assets' );

/**
 * preconnect לפונטים — ביצועים (CWV).
 */
function niv_resource_hints( $hints, $relation ) {
	if ( 'preconnect' === $relation ) {
		$hints[] = array( 'href' => 'https://fonts.gstatic.com', 'crossorigin' );
	}
	return $hints;
}
add_filter( 'wp_resource_hints', 'niv_resource_hints', 10, 2 );

/**
 * ACF Local JSON — שמירה/טעינה מ-inc/acf-json (version control).
 */
function niv_acf_json_save( $path ) {
	return NIV_DIR . '/inc/acf-json';
}
add_filter( 'acf/settings/save_json', 'niv_acf_json_save' );

function niv_acf_json_load( $paths ) {
	$paths[] = NIV_DIR . '/inc/acf-json';
	return $paths;
}
add_filter( 'acf/settings/load_json', 'niv_acf_json_load' );

/**
 * עמוד הגדרות עסק (Options) — מקור NAP/CTA גלובלי.
 */
function niv_acf_options() {
	if ( function_exists( 'acf_add_options_page' ) ) {
		acf_add_options_page( array(
			'page_title' => __( 'ניב · הגדרות עסק', 'niv' ),
			'menu_title' => __( 'הגדרות עסק', 'niv' ),
			'menu_slug'  => 'niv-business',
			'icon_url'   => 'dashicons-admin-network',
			'position'   => 2,
			'capability' => 'manage_options',
		) );
	}
}
add_action( 'acf/init', 'niv_acf_options' );

/**
 * includes.
 */
require NIV_DIR . '/inc/cpt.php';
require NIV_DIR . '/inc/template-tags.php';
require NIV_DIR . '/inc/schema.php';
require NIV_DIR . '/inc/seo.php';
require NIV_DIR . '/inc/tracking.php';
require NIV_DIR . '/inc/content-guards.php';
if ( is_admin() ) {
	require NIV_DIR . '/inc/qa.php';
}
