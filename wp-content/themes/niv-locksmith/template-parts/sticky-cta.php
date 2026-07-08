<?php
/**
 * CTA דביק תחתון בנייד — חיוג + WhatsApp. עקרון מותג: זמינים בלחיצה אחת בנייד.
 * מוסתר בדסקטופ (CSS). לא חוסם תוכן (padding-bottom על body בנייד).
 *
 * @package niv
 */

$ctx = niv_page_context();
$has_wa = (bool) preg_replace( '/\D/', '', niv_whatsapp_e164() );
?>
<div class="niv-sticky-cta" role="region" aria-label="<?php esc_attr_e( 'פעולות מהירות', 'niv' ); ?>">
	<?php if ( niv_has_phone() ) : ?>
	<a class="niv-sticky-cta__btn niv-sticky-cta__btn--call js-sticky-cta js-call-click"
	   href="tel:<?php echo esc_attr( niv_phone_e164() ); ?>"
	   data-cta-location="sticky" data-cta-type="call"
	   data-service="<?php echo esc_attr( $ctx['service'] ); ?>" data-area="<?php echo esc_attr( $ctx['area'] ); ?>"
	   data-phone="<?php echo esc_attr( niv_phone_e164() ); ?>"
	   aria-label="<?php esc_attr_e( 'חייגו לניב עכשיו', 'niv' ); ?>">
		<span aria-hidden="true"><?php echo niv_icon( 'phone' ); ?></span>
		<span>חייגו עכשיו</span>
	</a>
	<?php endif; ?>

	<?php if ( $has_wa ) :
		$wa = preg_replace( '/\D/', '', niv_whatsapp_e164() );
		$msg = rawurlencode( 'שלום ניב, צריך/ה מנעולן' . ( $ctx['area'] ? ' ב' . $ctx['area'] : ' בירושלים' ) );
	?>
	<a class="niv-sticky-cta__btn niv-sticky-cta__btn--wa js-sticky-cta js-whatsapp-click"
	   href="https://wa.me/<?php echo esc_attr( $wa ); ?>?text=<?php echo esc_attr( $msg ); ?>"
	   target="_blank" rel="noopener"
	   data-cta-location="sticky" data-cta-type="whatsapp"
	   data-service="<?php echo esc_attr( $ctx['service'] ); ?>" data-area="<?php echo esc_attr( $ctx['area'] ); ?>"
	   aria-label="<?php esc_attr_e( 'שליחת וואטסאפ לניב', 'niv' ); ?>">
		<span aria-hidden="true"><?php echo niv_icon( 'whatsapp' ); ?></span>
		<span>WhatsApp</span>
	</a>
	<?php endif; ?>
</div>
