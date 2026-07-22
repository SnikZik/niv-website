# -*- coding: utf-8 -*-
import re,json

src=open('/Users/s/niv-locksmith/index.html',encoding='utf-8').read()
style=re.search(r'<style>.*?</style>',src,re.S).group(0)
ub=re.search(r'<div class="ub">.*?</div></div>',src,re.S).group(0)
header=re.search(r'<header class="hd">.*?</header>',src,re.S).group(0)
footer=re.search(r'<footer class="ft">.*?</footer>',src,re.S).group(0)
flt=re.search(r'<div class="float">.*?</div>\s*(?=<div class="smob">)',src,re.S).group(0)
smob=re.search(r'<div class="smob">.*?</div>\s*(?=</div>)',src,re.S).group(0)
js=re.search(r'<script>.*?</script>',src,re.S).group(0)
hero2=re.search(r'src="(data:[^"]+)" alt="ניב, מנעולן בירושלים',src).group(1)
BASE='https://snikzik.github.io/niv-website'
WAURL='https://wa.me/972508307269?text=%D7%A9%D7%9C%D7%95%D7%9D%20%D7%A0%D7%99%D7%91'

extra='''
.n6 .bc{background:#fff;border-bottom:1px solid var(--line);font-size:13.5px;padding:8px 0}
.n6 .bc .wrap{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.n6 .bc a{color:var(--iron)} .n6 .bc b{color:var(--ink);font-weight:700}
.n6 .phero{background:linear-gradient(180deg,#EAF1F7,#fff);padding:36px 0 30px;border-bottom:1px solid var(--line)}
.n6 .phero h1{font-size:33px;margin-bottom:10px}
.n6 .phero p{font-size:17px;color:var(--iron);max-width:640px;line-height:1.65}
.n6 .content{max-width:760px;margin-inline:auto;padding:36px 22px}
.n6 .content h2{font-size:24px;margin:28px 0 10px}
.n6 .content h2:first-child{margin-top:0}
.n6 .content p{font-size:16.5px;line-height:1.75;margin-bottom:12px}
.n6 .content ul{margin:0 0 14px;padding-inline-start:22px}
.n6 .content li{font-size:16px;line-height:1.7;margin-bottom:6px}
.n6 .content a{color:var(--red);font-weight:700;text-decoration:underline;text-underline-offset:3px}
.n6 .content a.btn{text-decoration:none}
.n6 .content a.btn--call{color:#fff}
.n6 .content a.btn--wa{color:#fff}
.n6 .cways{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:20px 0}
.n6 .cway{background:#fff;border:1px solid var(--line);border-radius:14px;padding:22px;box-shadow:var(--sh);text-align:center}
.n6 .cway b{display:block;font-size:17px;margin-bottom:6px}
.n6 .cway p{color:var(--iron);font-size:14px;margin:0 0 14px}
.n6 .cway .btn{width:100%;justify-content:center}
@media(max-width:640px){.n6 .cways{grid-template-columns:1fr}.n6 .phero h1{font-size:27px}}
'''
style=style.replace('</style>',extra+'\n</style>')

def shell(slug,title,meta,h1,intro,main,ld=None):
    lds='<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>' if ld else ''
    html=f'''<!doctype html>
<html dir="rtl" lang="he">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="{BASE}/{slug}.html">
{lds}
{style}
</head>
<body>
<div class="n6">
{ub}
{header}
  <nav class="bc" aria-label="פירורי לחם"><div class="wrap"><a href="/">בית</a><span aria-hidden="true">›</span><b>{h1}</b></div></nav>
  <section class="phero"><div class="wrap"><h1>{h1}</h1><p>{intro}</p></div></section>
{main}
{footer}
{flt}
{smob}
</div>
{js}
</body>
</html>'''
    open(f'/Users/s/niv-locksmith/{slug}.html','w',encoding='utf-8').write(html)
    print(slug,'| title',len(title),'| meta',len(meta))

CTA=f'''<section class="sec fcta" style="text-align:center;padding:48px 22px">
    <h2 style="font-size:26px;margin-bottom:10px">צריכים מנעולן בירושלים?</h2>
    <p style="margin-bottom:20px;font-size:17px">חייגו, תארו מה קרה, ותקבלו מחיר וזמן הגעה כבר בשיחה.</p>
    <div class="btnrow" style="justify-content:center">
      <a class="btn btn--call btn--lg" href="tel:+972508307269">חייגו 050-8307269</a>
      <a class="btn btn--wa btn--lg" href="{WAURL}" target="_blank" rel="noopener">שלחו WhatsApp</a>
    </div>
  </section>'''

# ---------- 1. contact ----------
main=f'''
  <div class="content">
    <div class="cways">
      <div class="cway"><b>הכי מהיר, טלפון</b><p>עונה בעצמי, 24/7 כולל לילות ושבתות</p><a class="btn btn--call" href="tel:+972508307269">חייגו 050-8307269</a></div>
      <div class="cway"><b>WhatsApp עם צילום</b><p>שלחו תמונה של הדלת ותקבלו הערכה מדויקת</p><a class="btn btn--wa" href="{WAURL}" target="_blank" rel="noopener">שלחו הודעה</a></div>
    </div>
    <h2>לא דחוף? השאירו פרטים</h2>
    <p>אחזור אליכם בהקדם עם הסבר וכיוון. אפשר לציין מה סוג הדלת והתקלה.</p>
    <form class="cbform" onsubmit="return false" style="margin-top:14px">
      <div><label for="c-name">שם</label><input id="c-name" type="text" name="name" autocomplete="name" required></div>
      <div><label for="c-phone">טלפון</label><input id="c-phone" type="tel" name="phone" autocomplete="tel" required placeholder="050-0000000"></div>
      <div><label for="c-area">אזור / עיר</label><input id="c-area" type="text" name="area" autocomplete="address-level2" placeholder="למשל: פסגת זאב"></div>
      <div><label for="c-msg">מה קרה?</label><input id="c-msg" type="text" name="msg" placeholder="דלת נטרקה, צילינדר תקוע..."></div>
      <div class="full"><button class="btn btn--call" type="submit" style="width:100%">שלחו, וניב יחזור אליכם</button></div>
      <div class="hint">הפרטים נשלחים לניב בלבד ומשמשים ליצירת קשר. <a href="/mediniyut-pratiut.html">מדיניות פרטיות</a></div>
    </form>
    <h2>אזורי שירות</h2>
    <p>כל שכונות ירושלים, גבעת זאב, מבשרת ציון ומעלה אדומים. מגיע עד אליכם, בדרך כלל תוך כ-20 דקות בתוך העיר.</p>
    <h2>שעות פעילות</h2>
    <p>אני זמין 24 שעות ביממה, 7 ימים בשבוע, כולל שבתות וחגים. דלת נעולה לא בוחרת שעה, ולכן גם אני לא.</p>
  </div>'''
ld={"@context":"https://schema.org","@type":"ContactPage","name":"צור קשר, ניב המנעולן","url":BASE+"/tzor-kesher.html",
 "mainEntity":{"@type":"Locksmith","name":"ניב המנעולן","telephone":"+972508307269","address":{"@type":"PostalAddress","addressLocality":"ירושלים","addressCountry":"IL"}}}
shell("tzor-kesher","צור קשר | ניב המנעולן, מנעולן בירושלים 050-8307269",
 "צרו קשר עם ניב המנעולן בירושלים. טלפון 050-8307269, וואטסאפ עם צילום, או השארת פרטים. זמין 24/7 בכל שכונות ירושלים והסביבה.",
 "צור קשר","הדרך הכי מהירה היא להתקשר. עונה בעצמי, בלי מוקד, ואומר לכם מחיר וזמן הגעה כבר בשיחה.",main,ld)

# ---------- 2. accessibility ----------
main='''
  <div class="content">
    <p>אתר זה של ניב המנעולן נבנה מתוך כוונה לאפשר לכל אדם, כולל אנשים עם מוגבלות, לגלוש בו בנוחות. אנחנו פועלים בהתאם להנחיות הנגישות WCAG 2.1 ברמה AA ולתקן הישראלי ת״י 5568.</p>
    <h2>מה עשינו באתר</h2>
    <ul>
      <li>ניגודיות צבעים העומדת בדרישות AA בכל הטקסטים והכפתורים</li>
      <li>ניווט מלא במקלדת, כולל סימון פוקוס ברור בכל רכיב</li>
      <li>תיאורי alt לכל התמונות ותוויות aria לכפתורים</li>
      <li>מבנה כותרות תקין והיררכי בכל עמוד</li>
      <li>שדות טופס עם תוויות מקושרות</li>
      <li>אזורי לחיצה בגודל נוח למגע</li>
      <li>כיבוד העדפת reduced motion למשתמשים הרגישים לאנימציה</li>
      <li>טקסט קריא בגודל 16 פיקסלים ומעלה</li>
    </ul>
    <h2>נתקלתם בבעיה?</h2>
    <p>אם נתקלתם בקושי נגישות באתר, נשמח לשמוע ולתקן. אפשר לפנות בטלפון <a href="tel:+972508307269">050-8307269</a> או בוואטסאפ, ונטפל בפנייה בהקדם.</p>
    <h2>פרטי רכז הנגישות</h2>
    <p>ניב, טלפון 050-8307269. הצהרה זו עודכנה ביולי 2026.</p>
  </div>'''
shell("hazharat-negishut","הצהרת נגישות | ניב המנעולן",
 "הצהרת הנגישות של אתר ניב המנעולן. האתר נבנה לפי הנחיות WCAG 2.1 AA ות״י 5568. נתקלתם בבעיה? חייגו 050-8307269 ונתקן.",
 "הצהרת נגישות","האתר נבנה כך שכל אדם יוכל להשתמש בו בנוחות. כך עשינו את זה, ולמי לפנות אם משהו לא עובד.",main)

# ---------- 3. privacy ----------
main='''
  <div class="content">
    <p>הפרטיות שלכם חשובה. העמוד הזה מסביר בשפה פשוטה איזה מידע נאסף באתר של ניב המנעולן ומה נעשה איתו.</p>
    <h2>איזה מידע נאסף</h2>
    <ul>
      <li><b>פרטים שאתם משאירים.</b> שם, טלפון ותיאור התקלה שאתם ממלאים בטופס או שולחים בוואטסאפ.</li>
      <li><b>מידע טכני בסיסי.</b> כמו בכל אתר, שרת האחסון שומר יומני גישה סטנדרטיים.</li>
    </ul>
    <h2>מה נעשה עם המידע</h2>
    <ul>
      <li>הפרטים משמשים אך ורק לחזרה אליכם ולמתן השירות שביקשתם.</li>
      <li>המידע לא נמכר, לא מועבר ולא נמסר לגורם שלישי.</li>
      <li>אין דיוור פרסומי. אם השארתם טלפון, תקבלו שיחה אחת חוזרת מניב ולא שום דבר אחר.</li>
    </ul>
    <h2>עוגיות</h2>
    <p>האתר לא עושה שימוש בעוגיות פרסום ולא עוקב אחריכם. אם בעתיד יתווסף כלי מדידה בסיסי, העמוד הזה יעודכן בהתאם.</p>
    <h2>יצירת קשר בנושא פרטיות</h2>
    <p>לשאלות או בקשה למחיקת פרטים, חייגו <a href="tel:+972508307269">050-8307269</a>. עודכן ביולי 2026.</p>
  </div>'''
shell("mediniyut-pratiut","מדיניות פרטיות | ניב המנעולן",
 "מדיניות הפרטיות של אתר ניב המנעולן. איזה מידע נאסף, מה נעשה איתו ולמי לפנות. הפרטים משמשים ליצירת קשר בלבד ולא מועברים לאיש.",
 "מדיניות פרטיות","בשפה פשוטה, איזה מידע נאסף באתר ומה נעשה איתו.",main)

# ---------- 4. about ----------
main=f'''
  <section class="about" style="border-bottom:1px solid var(--line)"><div class="wrap"><div class="about__in">
    <div class="about__img"><img src="{hero2}" alt="ניב, מנעולן בירושלים, עובד על מנגנון של דלת"></div>
    <div>
      <h2>נעים להכיר</h2>
      <p>אני ניב, מנעולן שעובד בירושלים והסביבה. רוב הקריאות שאני מקבל מגיעות ברגעים הכי לא נוחים, דלת שנטרקה, צילינדר תקוע, מפתח שנשבר או דלת שלא ננעלת.</p>
      <p class="m">קודם אני מבין מה התקלה, מסביר מה הפתרון וכמה יעלה, ורק אז מתחיל לעבוד. אתם מדברים ישירות איתי, מהשיחה הראשונה ועד שהדלת נסגרת מאחוריי.</p>
    </div>
  </div></div></section>
  <div class="content">
    <h2>איך אני עובד</h2>
    <ul>
      <li><b>מחיר לפני עבודה.</b> המחיר נסגר בטלפון, לפני שאני יוצא. לא מתחיל בלי שאישרתם.</li>
      <li><b>קודם לתקן, אחר כך להחליף.</b> אני מעדיף לפתוח בזהירות ולתקן. החלפה רק כשבאמת צריך, ואז אסביר למה.</li>
      <li><b>בלי מוקד ובלי קבלני משנה.</b> מי שעונה לטלפון הוא מי שמגיע לדלת. זה אני.</li>
      <li><b>זמין 24/7.</b> לילות, שבתות וחגים. בתוך ירושלים אני בדרך כלל אצלכם תוך כ-20 דקות.</li>
    </ul>
    <h2>מה אני עושה</h2>
    <p><a href="/pritzat-dlatot.html">פריצת דלתות</a>, <a href="/tzilinder.html">החלפת צילינדרים</a>, <a href="/tikun-dlatot.html">תיקון דלתות</a>, <a href="/mamad.html">דלתות ממ״ד</a>, <a href="/ksafot.html">כספות</a>, <a href="/manul-hacham.html">מנעולים חכמים</a>, <a href="/mahzirei-delet.html">מחזירי דלת</a>, <a href="/electromagnet.html">אלקטרומגנטים</a>, <a href="/yadiyot-bahala.html">ידיות בהלה</a>, <a href="/pladelet.html">דלתות פלדלת</a> ו<a href="/rav-bariach.html">מנעולי רב בריח</a>.</p>
    <h2>איפה אני עובד</h2>
    <p>בכל שכונות ירושלים, מפסגת זאב ורמות בצפון ועד גילה והר חומה בדרום, וגם בגבעת זאב, מבשרת ציון ומעלה אדומים. רוב הלקוחות שלי מגיעים דרך המלצות של לקוחות קודמים ושכנים.</p>
  </div>'''+CTA
shell("odot","אודות ניב המנעולן | מנעולן לדלתות בירושלים",
 "מי זה ניב המנעולן? מנעולן מקומי בירושלים, בלי מוקד ובלי קבלני משנה. מחיר נסגר בטלפון, זמין 24/7, רוב הלקוחות מגיעים בהמלצה. 050-8307269.",
 "אודות ניב","מנעולן מקומי בירושלים. מי שעונה לטלפון הוא מי שמגיע לדלת.",main)

# ---------- 5. pricing ----------
rows=[["פריצת דלת","החל מ-300₪"],["החלפת צילינדר לדלת","החל מ-300₪"],["החלפת צילינדר לדלת פלדלת","החל מ-350₪"],["החלפת ידיות","החל מ-250₪"],["תיקון דלתות","החל מ-350₪"],["התקנת מנעול מכני לדלת","החל מ-550₪"],["התקנת דלת ממ״ד","החל מ-650₪"],["תיקון דלת ממ״ד","החל מ-350₪"],["פריצת כספות","החל מ-350₪"],["התקנת כספת (כולל הכספת)","החל מ-499₪"],["התקנת מנעול חכם","החל מ-1,499₪"]]
trows="".join(f'<div class="prow"><span class="prow__s">{a}</span><span class="prow__p">{b}</span></div>' for a,b in rows)
main=f'''
  <section class="sec sec--white" style="padding-top:34px"><div class="wrap narrow">
    <div class="ptable">{trows}</div>
    <p class="pnote">כל המחירים הם ״החל מ-״. המחיר המדויק נסגר בטלפון לפני שאני יוצא, ולא משתנה בשטח.</p>
  </div></section>
  <div class="content" style="padding-top:10px">
    <h2>מה קובע את המחיר הסופי</h2>
    <ul>
      <li><b>סוג הדלת.</b> דלת עץ פשוטה מול פלדלת עם רב בריח או דלת ממ״ד.</li>
      <li><b>סוג הנעילה.</b> צילינדר רגיל, צילינדר מוגן או מנגנון מורכב.</li>
      <li><b>מצב התקלה.</b> מפתח שבור בפנים או מנגנון תקוע דורשים עבודה עדינה יותר.</li>
      <li><b>שעה ומקום.</b> קריאת לילה או יישוב מחוץ לירושלים יכולים להוסיף מעט, ואני אומר את זה מראש בטלפון.</li>
    </ul>
    <h2>למה אצלי אין הפתעות</h2>
    <p>המחיר נסגר בשיחה, לפני שאני יוצא אליכם. אני שואל מה קרה ואיזו דלת יש, נותן מחיר, ורק אחרי שאישרתם אני בדרך. הכי מדויק לשלוח לי <a href="{WAURL}">צילום בוואטסאפ</a> של הדלת והמנעול, ולקבל הערכה מלאה עוד לפני היציאה.</p>
  </div>'''+CTA
shell("mehiron","מחירון מנעולן בירושלים 2026 | ניב המנעולן",
 "מחירון מנעולן בירושלים: פריצת דלת מ-300₪, החלפת צילינדר מ-300₪, תיקון דלתות מ-350₪, מנעול חכם מ-1,499₪. המחיר נסגר בטלפון מראש.",
 "מחירון מנעולן בירושלים","מחירים אמיתיים, נסגרים בטלפון לפני שאני יוצא. בלי הפתעות בשטח.",main)

# ---------- 6. guides index ----------
main='''
  <section class="sec sec--white" style="padding-top:34px"><div class="wrap">
    <div class="bgrid">
      <div class="bpost"><div class="k">פריצת דלתות</div><h3><a href="/delet-nitreka.html">הדלת נטרקה והמפתח בפנים, מה עושים?</a></h3><p>מה לעשות בדקות הראשונות, מה אסור לנסות, ואיך לא ליפול על מוקד ארצי.</p><a class="l" href="/delet-nitreka.html">לקריאה ›</a></div>
    </div>
    <p style="color:var(--iron);margin-top:26px;font-size:15px">מדריכים נוספים בדרך. בינתיים, אם יש שאלה על הדלת שלכם, פשוט תתקשרו ואענה.</p>
  </div></section>'''+CTA
shell("madrichim","מדריכי מנעולנות | ניב המנעולן ירושלים",
 "מדריכים מהשטח של ניב המנעולן: מה לעשות כשהדלת נטרקה, מתי מחליפים צילינדר וכמה עולה מנעולן בירושלים. בלי קיצורי דרך מסוכנים.",
 "מדריכי מנעולנות","תשובות אמיתיות מהשטח, בלי קיצורי דרך מסוכנים ובלי סיפורים.",main)

# ---------- 7. services hub ----------
cards=[("pritzat-dlatot","פריצת דלתות","ננעלתם בחוץ, המפתח אבד או נשבר בפנים."),
("tzilinder","החלפת צילינדר","צילינדר תקוע, ישן, או אחרי מעבר דירה."),
("tikun-dlatot","תיקון דלתות","דלת שלא ננעלת, ידית רפויה, מנגנון שנתקע."),
("mamad","פריצת דלת ממ״ד","דלת ממ״ד נעולה או מנגנון שנתקע."),
("ksafot","פריצת כספות","כספת ביתית או עסקית שלא נפתחת."),
("manul-hacham","מנעול חכם","מנעול קוד, טביעת אצבע או אפליקציה."),
("mahzirei-delet","מחזירי דלת","מחזיר עילי, נסתר או רצפתי, כולל כיוון."),
("electromagnet","אלקטרומגנט","נעילה מגנטית לכניסות בניין ומשרד."),
("yadiyot-bahala","ידיות בהלה","יציאות חירום לפי תקן, לעסקים ומוסדות."),
("pladelet","דלת פלדלת + משקוף","התקנה והחלפה של פלדלת, כולל המשקוף."),
("rav-bariach","מנעול רב בריח","רב בריח שנתקע או התיישן בפלדלת."),
("manulan-herum","מנעולן חירום 24/7","מגיע בדרך כלל תוך כ-20 דקות, יום ולילה.")]
scards="".join(f'<a class="scard" href="/{s}.html"><h3>{t}</h3><p>{p}</p><span class="scard__l">לעמוד השירות ›</span></a>' for s,t,p in cards)
main=f'''
  <section class="sec sec--white" style="padding-top:34px"><div class="wrap">
    <div class="scards">{scards}</div>
  </div></section>'''+CTA
shell("sherutim","שירותי מנעולן בירושלים | ניב המנעולן",
 "כל שירותי המנעולנות של ניב בירושלים: פריצת דלתות, צילינדרים, תיקון דלתות, ממ״ד, כספות, מנעולים חכמים, מחזירי דלת וידיות בהלה.",
 "שירותי מנעולן בירושלים","כל תקלת דלת ומנעול, בבית ובעסק. לחצו על שירות למחירים ופרטים.",main)

# ---------- 8. areas hub ----------
main='''
  <div class="content">
    <p>אני עובד בכל שכונות ירושלים וביישובים סביב העיר. אין תוספת ״אזור מרוחק״ בתוך ירושלים, והמחיר נסגר בטלפון מראש. בתוך העיר אני מגיע בדרך כלל תוך כ-20 דקות.</p>
    <h2>שכונות ירושלים</h2>
    <p>פסגת זאב · נווה יעקב · רמות · רמת שלמה · גבעה צרפתית · בית הכרם · קריית יובל · קריית מנחם · עיר גנים · גילה · הר חומה · תלפיות · ארנונה · בקעה · קטמון · רחביה · נחלאות · מרכז העיר · גאולה · רוממה · הר נוף · גבעת שאול · גבעת מרדכי · מלחה · רמת רחל</p>
    <h2>יישובים בסביבה</h2>
    <p>גבעת זאב · מבשרת ציון · מעלה אדומים · אבו גוש · הראל · מוצא</p>
    <h2>למה מנעולן מקומי עדיף</h2>
    <p>מנעולן שעובד בירושלים כל יום מכיר את סוגי הדלתות והבניינים בכל שכונה. פלדלת ישנה בקטמון מתנהגת אחרת מדלת חדשה בהר חומה, וזה משפיע על הדרך הנכונה לפתוח בזהירות. וכשאני קרוב, אני גם מגיע מהר.</p>
  </div>'''+CTA
shell("azorei-sherut","אזורי שירות | מנעולן בירושלים והסביבה, ניב",
 "ניב המנעולן עובד בכל שכונות ירושלים, גבעת זאב, מבשרת ציון ומעלה אדומים. הגעה כ-20 דקות בתוך העיר, מחיר נסגר בטלפון. 050-8307269.",
 "אזורי שירות","כל שכונות ירושלים והיישובים סביב. מגיע עד אליכם, מהר.",main)
