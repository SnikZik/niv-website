<?php
/**
 * GTM injection + הקשר עמוד ל-dataLayer. פעם אחת בלבד.
 *
 * @package niv
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * GTM head — עם dataLayer ראשוני (הקשר עמוד).
 */
function niv_gtm_head() {
	$gtm = niv_biz( 'biz_gtm' );
	if ( ! $gtm ) {
		return;
	}
	$ctx = niv_page_context();
	?>
<script>
window.dataLayer = window.dataLayer || [];
window.dataLayer.push({
	'page_type': '<?php echo esc_js( niv_current_page_type() ); ?>',
	'service': '<?php echo esc_js( $ctx['service'] ); ?>',
	'area': '<?php echo esc_js( $ctx['area'] ); ?>'
});
</script>
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','<?php echo esc_js( $gtm ); ?>');</script>
<!-- End Google Tag Manager -->
	<?php
}
add_action( 'wp_head', 'niv_gtm_head', 2 );

/**
 * GTM noscript אחרי פתיחת body.
 */
function niv_gtm_body() {
	$gtm = niv_biz( 'biz_gtm' );
	if ( ! $gtm ) {
		return;
	}
	printf(
		'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=%s" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>',
		esc_attr( $gtm )
	);
}
add_action( 'wp_body_open', 'niv_gtm_body' );

/**
 * סוג העמוד ל-dataLayer.
 */
function niv_current_page_type() {
	if ( is_front_page() ) { return 'home'; }
	if ( is_singular( 'service' ) ) { return 'service'; }
	if ( is_singular( 'service_area' ) ) { return 'service_area'; }
	if ( is_singular( 'service_area_page' ) ) { return 'service_area_page'; }
	if ( is_singular( 'post' ) ) { return 'guide'; }
	if ( is_page() ) { return 'page'; }
	if ( is_archive() ) { return 'archive'; }
	return 'other';
}
