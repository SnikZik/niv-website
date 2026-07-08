<?php
/**
 * עמוד הבית — ממוקד המרה. H1 = מנעולן לדלתות בירושלים.
 * תוכן בקול המותג (docs/00). שירותים/אזורים נשלפים דינמית עם fallback.
 *
 * @package niv
 */

get_header();

// שירותים לכרטיסים (עד 6). fallback לרשימה קבועה אם ה-DB ריק.
$services = get_posts( array( 'post_type' => 'service', 'numberposts' => 6, 'post_status' => 'publish', 'orderby' => 'menu_order', 'order' => 'ASC' ) );
$fallback_services = array(
	array( 'icon' => 'key',    'title' => 'פריצת דלתות', 'desc' => 'ננעלתם בחוץ או שהמפתח נשבר? פותחים בזהירות, בלי נזק מיותר לדלת.' ),
	array( 'icon' => 'lock',   'title' => 'החלפת צילינדר', 'desc' => 'צילינדר שנתקע, התיישן או אחרי דירה שכורה. מחליפים למנעול שמתאים לדלת.' ),
	array( 'icon' => 'shield', 'title' => 'פריצת דלת ממ״ד', 'desc' => 'דלת ממ״ד נעולה עם מפתח בפנים? מטפלים בעדינות במנגנון המיוחד שלה.' ),
	array( 'icon' => 'lock',   'title' => 'תיקון דלתות', 'desc' => 'דלת שלא ננעלת, ידית רפויה או מנגנון תקוע. בודקים ומתקנים בשטח.' ),
	array( 'icon' => 'shield', 'title' => 'פריצת כספות', 'desc' => 'כספת ביתית או עסקית שלא נפתחת. ניגשים בזהירות לפי סוג הכספת.' ),
	array( 'icon' => 'key',    'title' => 'מנעול חכם', 'desc' => 'התקנה והחלפה של מנעולים חכמים לדלת הכניסה, עם הסבר איך משתמשים.' ),
);

// אזורים לגריד.
$areas = get_posts( array( 'post_type' => 'service_area', 'numberposts' => 12, 'post_status' => 'publish' ) );
$fallback_areas = array( 'ירושלים', 'גבעת זאב', 'מבשרת ציון', 'מעלה אדומים', 'פסגת זאב', 'רמות', 'גילה', 'תלפיות', 'קטמון', 'בית הכרם', 'קריית יובל', 'נווה יעקב' );
?>

<main id="niv-main">

	<!-- ===== הירו חירום ===== -->
	<section class="niv-hero">
		<?php
		// תמונת אמת של ניב/עבודה — NEEDS_CLIENT_INPUT. עד אז רקע כהה בלבד.
		$hero_img = niv_biz( 'biz_hero_image' );
		if ( $hero_img && is_array( $hero_img ) ) :
			printf( '<div class="niv-hero__media"><img src="%s" alt="" loading="eager" fetchpriority="high"></div>', esc_url( $hero_img['url'] ) );
		endif;
		?>
		<div class="niv-container niv-hero__inner">
			<div class="niv-hero__content">
				<h1>מנעולן לדלתות בירושלים</h1>
				<p class="niv-hero__sub">נתקעתם מחוץ לדלת, הדלת נטרקה או הצילינדר לא מסתובב? ניב נותן מענה מהיר לדלתות, צילינדרים ומנגנונים באזור ירושלים והסביבה.</p>
				<div class="niv-btn-row">
					<?php niv_call_button( array( 'location' => 'hero', 'text' => 'חייגו עכשיו', 'class' => 'niv-btn--lg' ) ); ?>
					<?php niv_whatsapp_button( array( 'location' => 'hero', 'class' => 'niv-btn--lg' ) ); ?>
				</div>
				<p class="niv-hero__note">נעולים בחוץ? ניב כבר בדרך. מנעול נפתח, ראש נרגע.</p>
			</div>
		</div>
	</section>

	<!-- ===== שורת אמון ===== -->
	<div class="niv-container">
		<div class="niv-trust">
			<span class="niv-trust__item"><?php echo niv_icon( 'clock' ); ?> מענה מהיר באזור ירושלים</span>
			<span class="niv-trust__item"><?php echo niv_icon( 'lock' ); ?> דלתות, צילינדרים ומנגנונים</span>
			<span class="niv-trust__item"><?php echo niv_icon( 'shield' ); ?> הסבר מחיר לפני העבודה</span>
			<span class="niv-trust__item"><?php echo niv_icon( 'key' ); ?> עבודה נקייה ככל האפשר</span>
		</div>
	</div>

	<!-- ===== כרטיסי שירות ===== -->
	<section class="niv-section niv-section--alt">
		<div class="niv-container">
			<div class="niv-section__head">
				<h2>השירותים של ניב</h2>
				<p>מטפלים בכל תקלת נעילה בבית ובעסק — מהדלת שנטרקה ועד הצילינדר שצריך החלפה.</p>
			</div>
			<div class="niv-cards">
				<?php if ( $services ) : ?>
					<?php foreach ( $services as $s ) :
						$sicon = get_field( 'schema_service_type', $s->ID ) ? 'lock' : 'lock';
						?>
						<article class="niv-card">
							<div class="niv-card__icon"><?php echo niv_icon( 'lock' ); ?></div>
							<h3><a href="<?php echo esc_url( get_permalink( $s ) ); ?>" class="js-service-card" data-service="<?php echo esc_attr( get_the_title( $s ) ); ?>"><?php echo esc_html( get_the_title( $s ) ); ?></a></h3>
							<p><?php echo esc_html( get_field( 'short_desc', $s->ID ) ?: wp_trim_words( $s->post_excerpt, 18 ) ); ?></p>
							<a class="niv-card__link js-service-card" data-service="<?php echo esc_attr( get_the_title( $s ) ); ?>" href="<?php echo esc_url( get_permalink( $s ) ); ?>">לפרטים ‹</a>
						</article>
					<?php endforeach; ?>
				<?php else : ?>
					<?php foreach ( $fallback_services as $s ) : ?>
						<article class="niv-card">
							<div class="niv-card__icon"><?php echo niv_icon( $s['icon'] ); ?></div>
							<h3><?php echo esc_html( $s['title'] ); ?></h3>
							<p><?php echo esc_html( $s['desc'] ); ?></p>
							<span class="niv-card__link niv-muted">בקרוב עמוד ייעודי</span>
						</article>
					<?php endforeach; ?>
				<?php endif; ?>
			</div>
		</div>
	</section>

	<!-- ===== למה ניב ===== -->
	<section class="niv-section niv-section--dark">
		<div class="niv-container">
			<div class="niv-section__head">
				<h2>למה ניב המנעולן</h2>
				<p>לא מוכרים פחד. מוכרים ראש שקט.</p>
			</div>
			<div class="niv-features">
				<div class="niv-feature">
					<span class="niv-feature__icon"><?php echo niv_icon( 'clock' ); ?></span>
					<h3>מגיעים מהר</h3>
					<p>אנחנו מקומיים ומכירים כל שכונה וכל בניין בירושלים, אז מגיעים אליכם מהר.</p>
				</div>
				<div class="niv-feature">
					<span class="niv-feature__icon"><?php echo niv_icon( 'shield' ); ?></span>
					<h3>אומרים מחיר מראש</h3>
					<p>מסבירים מה התקלה ומה המחיר עוד לפני שמתחילים. בלי הפתעות בסוף.</p>
				</div>
				<div class="niv-feature">
					<span class="niv-feature__icon"><?php echo niv_icon( 'key' ); ?></span>
					<h3>פותחים בעדינות</h3>
					<p>הכלים הנכונים לכל סוג מנעול, כדי לפתוח בלי לגרום נזק מיותר לדלת.</p>
				</div>
				<div class="niv-feature">
					<span class="niv-feature__icon"><?php echo niv_icon( 'home' ); ?></span>
					<h3>מדברים בגובה העיניים</h3>
					<p>שיחה רגועה, בלי לחץ. קודם מבינים מה קרה, ואז מחליטים ביחד מה עושים.</p>
				</div>
			</div>
		</div>
	</section>

	<!-- ===== הסבר חירום — כך זה עובד ===== -->
	<section class="niv-section">
		<div class="niv-container niv-narrow">
			<h2>נתקעתם בחוץ? ככה זה עובד</h2>
			<p>רוב הקריאות שלנו הן רגעים לא נעימים — דלת שנטרקה עם המפתח בפנים, צילינדר שהתחיל להסתובב על ריק, או ידית שנשברה בדיוק כשמיהרתם. הדבר הראשון, לא להפעיל כוח על הידית. זה בדרך כלל רק מחמיר את המצב.</p>
			<ol>
				<li><strong>מתקשרים או שולחים צילום ב-WhatsApp.</strong> כבר בשיחה ננסה להבין מה קרה ומה סוג הדלת.</li>
				<li><strong>מקבלים הסבר והערכת מחיר.</strong> אומרים מראש מה הולך לקרות וכמה זה עולה.</li>
				<li><strong>ניב מגיע ופותח.</strong> בוחרים את הדרך הנכונה לפתוח או לתקן, בלי נזק מיותר.</li>
			</ol>
			<div class="niv-btn-row" style="margin-top:1.5rem">
				<?php niv_call_button( array( 'location' => 'how-it-works', 'text' => 'חייגו לניב עכשיו' ) ); ?>
				<?php niv_whatsapp_button( array( 'location' => 'how-it-works', 'text' => 'שלחו צילום של הדלת' ) ); ?>
			</div>
		</div>
	</section>

	<!-- ===== אזורי שירות ===== -->
	<section class="niv-section niv-section--alt">
		<div class="niv-container">
			<div class="niv-section__head">
				<h2>אזורי שירות בירושלים והסביבה</h2>
				<p>נותנים מענה בשכונות ירושלים ובערים סביב העיר.</p>
			</div>
			<div class="niv-areas">
				<?php if ( $areas ) : ?>
					<?php foreach ( $areas as $a ) : ?>
						<a class="niv-area-chip js-area-card" data-area="<?php echo esc_attr( get_the_title( $a ) ); ?>" href="<?php echo esc_url( get_permalink( $a ) ); ?>">
							<?php echo niv_icon( 'home' ); ?><?php echo esc_html( get_the_title( $a ) ); ?>
						</a>
					<?php endforeach; ?>
				<?php else : ?>
					<?php foreach ( $fallback_areas as $a ) : ?>
						<span class="niv-area-chip niv-muted"><?php echo niv_icon( 'home' ); ?>מנעולן ב<?php echo esc_html( $a ); ?></span>
					<?php endforeach; ?>
				<?php endif; ?>
			</div>
		</div>
	</section>

	<!-- ===== סקשן מילת מפתח (תוכן SEO אנושי) ===== -->
	<section class="niv-section">
		<div class="niv-container niv-prose">
			<h2>מנעולן לדלתות בירושלים שאפשר לסמוך עליו</h2>
			<p>דלת היא הדבר שעומד בינכם לבין הבית, ולכן כשמשהו משתבש בה זה מרגיש דחוף. ניב המנעולן הוא שירות מנעולנות בירושלים שמתמחה בדיוק בזה — דלתות כניסה, צילינדרים ומנגנוני נעילה. בין אם מדובר בדלת פלדלת שלא נפתחת, צילינדר שצריך החלפה או מנעול רב בריח שהתקלקל, הכיוון תמיד אותו כיוון: להבין את התקלה, לפתוח או לתקן בלי נזק, ולהחזיר לכם את השקט.</p>
			<p>אנחנו עובדים בכל אזור ירושלים — ממרכז העיר, דרך פסגת זאב, רמות וגילה, ועד הערים שסביב כמו גבעת זאב, מבשרת ציון ומעלה אדומים. היתרון של מנעולן מקומי הוא פשוט: מכירים את סוגי הדלתות והבניינים באזור, ומגיעים מהר. אם אתם מחפשים מנעולן לדלתות בירושלים, אתם מוזמנים להתקשר או לשלוח צילום של הדלת, ונכוון אתכם כבר בשיחה.</p>
		</div>
	</section>

	<!-- ===== FAQ ===== -->
	<section class="niv-section niv-section--alt">
		<div class="niv-container">
			<?php
			$home_faq = array(
				array( 'q' => 'כמה מהר אפשר להגיע?', 'a' => 'תלוי איפה אתם ומה קורה באותו רגע. אנחנו מקומיים בירושלים, אז ברוב המקרים מגיעים מהר. הכי טוב להתקשר ולומר איפה אתם — ניתן לכם זמן הערכה אמיתי.' ),
				array( 'q' => 'אפשר לפתוח דלת בלי לשבור אותה?', 'a' => 'ברוב המקרים כן. אנחנו מגיעים עם הכלים המתאימים לכל סוג דלת ומנעול, והמטרה תמיד לפתוח בעדינות בלי נזק. יש מצבים שבהם צריך להחליף צילינדר אחרי הפתיחה, ועל זה נסביר מראש.' ),
				array( 'q' => 'איך יודעים כמה זה יעלה?', 'a' => 'אומרים לכם מחיר או הערכת מחיר עוד לפני שמתחילים לעבוד, לפי סוג התקלה והדלת. אנחנו לא מתחילים בלי שהבנתם מה הולך לקרות.' ),
				array( 'q' => 'אתם מטפלים גם בצילינדרים ובמנעולים חכמים?', 'a' => 'כן. מעבר לפתיחת דלתות, אנחנו מחליפים צילינדרים, מתקנים מנגנוני דלת ומתקינים מנעולים חכמים לדלת הכניסה.' ),
				array( 'q' => 'באילו אזורים אתם עובדים?', 'a' => 'בכל ירושלים והסביבה — שכונות העיר וגם ערים סמוכות כמו גבעת זאב, מבשרת ציון ומעלה אדומים.' ),
			);
			niv_render_faq( $home_faq );
			?>
		</div>
	</section>

	<!-- ===== תצוגת מדריכים ===== -->
	<?php
	$guides = get_posts( array( 'numberposts' => 3, 'post_status' => 'publish' ) );
	if ( $guides ) : ?>
	<section class="niv-section">
		<div class="niv-container">
			<div class="niv-section__head"><h2>מדריכים שימושיים</h2></div>
			<div class="niv-cards">
				<?php foreach ( $guides as $g ) : ?>
					<article class="niv-card">
						<h3><a href="<?php echo esc_url( get_permalink( $g ) ); ?>"><?php echo esc_html( get_the_title( $g ) ); ?></a></h3>
						<p><?php echo esc_html( wp_trim_words( get_the_excerpt( $g ), 20 ) ); ?></p>
						<a class="niv-card__link" href="<?php echo esc_url( get_permalink( $g ) ); ?>">לקריאה ‹</a>
					</article>
				<?php endforeach; ?>
			</div>
		</div>
	</section>
	<?php endif; ?>

	<!-- ===== CTA סופי ===== -->
	<section class="niv-section niv-cta-strip">
		<div class="niv-container niv-narrow">
			<h2>צריכים מנעולן בירושלים עכשיו?</h2>
			<p>התקשרו לניב, תארו מה קרה, וקבלו הערכת מחיר עוד לפני שמתחילים.</p>
			<div class="niv-btn-row">
				<?php niv_call_button( array( 'location' => 'footer-cta', 'text' => niv_has_phone() ? niv_phone_display() : 'חייגו עכשיו', 'class' => 'niv-btn--lg' ) ); ?>
				<?php niv_whatsapp_button( array( 'location' => 'footer-cta', 'class' => 'niv-btn--lg niv-btn--ghost-light' ) ); ?>
			</div>
		</div>
	</section>

</main>

<?php get_footer(); ?>
