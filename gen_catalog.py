# -*- coding: utf-8 -*-
import re,json,sys
sys.path.insert(0,'/Users/s/niv-locksmith')
from catalog_data import CATS
import json as _json
PIDX=_json.load(open('/Users/s/niv-locksmith/products_index.json',encoding='utf-8'))
try:
    from catalog_data2 import CATS2
    CATS={**CATS,**CATS2}
except ImportError:
    pass

src=open('/Users/s/niv-locksmith/index.html',encoding='utf-8').read()
style=re.search(r'<style>.*?</style>',src,re.S).group(0)
ub=re.search(r'<div class="ub">.*?</div></div>',src,re.S).group(0)
header=re.search(r'<header class="hd">.*?</header>',src,re.S).group(0)
footer=re.search(r'<footer class="ft">.*?</footer>',src,re.S).group(0)
flt=re.search(r'<div class="float">.*?</div>\s*(?=<div class="smob">)',src,re.S).group(0)
smob=re.search(r'<div class="smob">.*?</div>\s*(?=</div>)',src,re.S).group(0)
js=re.search(r'<script>.*?</script>',src,re.S).group(0)
BASE='https://snikzik.github.io/niv-website'
W='https://wa.me/972508307269?text=%D7%A9%D7%9C%D7%95%D7%9D%20%D7%A0%D7%99%D7%91'

cat_css='''
/* ===== v18: compact product cards, mobile 2-col ===== */
.n6 .pcard__img{height:112px}
@media(max-width:900px){
  .n6 .pgrid{grid-template-columns:1fr 1fr;gap:10px}
  .n6 .pgrid[style*="repeat(4"]{grid-template-columns:1fr 1fr !important}
  .n6 .pcard{padding:12px;gap:5px}
  .n6 .pcard__img{margin:-12px -12px 8px;height:92px}
  .n6 .pcard b{font-size:13px;line-height:1.3}
  .n6 .pcard p{font-size:11.5px;line-height:1.45}
  .n6 .pcard .ask{font-size:12px}
}

/* ===== catalog ===== */
.n6 .bc{background:#fff;border-bottom:1px solid var(--line);font-size:13.5px;padding:8px 0}
.n6 .bc .wrap{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.n6 .bc a{color:var(--iron)} .n6 .bc b{color:var(--ink);font-weight:700}
.n6 .phero{background:linear-gradient(180deg,#EAF1F7,#fff);padding:36px 0 30px;border-bottom:1px solid var(--line)}
.n6 .phero h1{font-size:33px;margin-bottom:10px}
.n6 .phero p{font-size:17px;color:var(--iron);max-width:680px;line-height:1.65}
.n6 .content{max-width:760px;margin-inline:auto;padding:36px 22px}
.n6 .content h2{font-size:24px;margin:28px 0 10px}
.n6 .content h2:first-child{margin-top:0}
.n6 .content p{font-size:16.5px;line-height:1.75;margin-bottom:12px}
.n6 .content ul{margin:0 0 14px;padding-inline-start:22px}
.n6 .content li{font-size:16px;line-height:1.7;margin-bottom:6px}
.n6 .content a{color:var(--red);font-weight:700;text-decoration:underline;text-underline-offset:3px}
.n6 .pgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.n6 .pcard{background:#fff;border:1px solid var(--line);border-radius:14px;padding:20px;box-shadow:var(--sh);display:flex;flex-direction:column;gap:7px}
.n6 .pcard b{font-size:16px;color:var(--ink);line-height:1.35}
.n6 .pcard p{color:var(--iron);font-size:13.5px;margin:0;line-height:1.5}
.n6 .pcard .tag{align-self:flex-start;background:var(--sand);border-radius:999px;font-size:11.5px;font-weight:700;color:var(--iron);padding:3px 10px}
.n6 .pcard .ask{margin-top:auto;padding-top:8px;font-size:13px;font-weight:800;color:var(--red)}
.n6 .pcard__img{margin:-20px -20px 10px;border-radius:14px 14px 0 0;overflow:hidden;height:130px;display:block}
.n6 .pcard__img img{width:100%;height:100%;object-fit:cover;display:block}
a.pcard{text-decoration:none}
.n6 .catgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.n6 .ccard{background:#fff;border:1px solid var(--line);border-radius:14px;padding:22px;box-shadow:var(--sh);display:flex;flex-direction:column;gap:6px}
.n6 .ccard b{font-size:17px}
.n6 .ccard p{color:var(--iron);font-size:13.5px;margin:0}
.n6 .ccard .n{color:var(--red);font-weight:800;font-size:12.5px}
.n6 .ccard .go{margin-top:auto;padding-top:8px;color:var(--red);font-weight:800;font-size:13.5px}
.n6 .revbox{background:var(--sand);border-radius:14px;padding:22px 24px;margin:18px 0}
.n6 .revbox h3{font-size:17px;margin-bottom:8px}
.n6 .revbox p{font-size:15px;color:var(--ink);margin-bottom:8px}
.n6 .revbox .src{font-size:12.5px;color:var(--iron)}
@media(max-width:900px){
  .n6 .pgrid{grid-template-columns:1fr 1fr}
  .n6 .catgrid{grid-template-columns:1fr 1fr}
  .n6 .phero h1{font-size:27px}
}
@media(max-width:560px){ .n6 .pgrid{grid-template-columns:1fr} }
'''
style=style.replace('</style>',cat_css+'\n</style>')

CTA=f'''<section class="sec fcta" style="text-align:center;padding:48px 22px">
    <h2 style="font-size:26px;margin-bottom:10px">רוצים להתייעץ לפני שבוחרים?</h2>
    <p style="margin-bottom:20px;font-size:17px">אני עוזר לבחור את המוצר הנכון לדלת ולתקציב, בלי למכור לכם את היקר ביותר סתם.</p>
    <div class="btnrow" style="justify-content:center">
      <a class="btn btn--call btn--lg" href="tel:+972508307269">חייגו 050-8307269</a>
      <a class="btn btn--wa btn--lg" href="{W}" target="_blank" rel="noopener">שלחו WhatsApp</a>
    </div>
  </section>'''


TOPUP={
 'katalog-avtacha-hachama':'לפני שסוגרים על דגם, שווה לבדוק מה קורה בבית כשאין חשמל או כשהסוללה נגמרת. כל המנעולים החכמים שאני מתקין כוללים פתרון גיבוי, מפתח מכני או חיבור סוללה חיצוני, ואני עובר על זה עם הלקוח בהתקנה עצמה. ככה לא נשארים בחוץ גם בתרחיש הכי פחות נעים.',
 'katalog-bakarat-knisa':'מערכת בקרת כניסה טובה נמדדת גם ביום שאחרי ההתקנה. הוספת דיירים, החלפת קודים וביטול תגים של שוכרים שעזבו צריכים להיות פעולות פשוטות שהוועד או המנהל עושים לבד. בהדרכה שאני נותן במסירה עוברים על כל התרחישים האלה בפועל, על המערכת עצמה.',
 'katalog-batei-malon':'בבתי מלון וצימרים הבלאי גבוה בהרבה מדירה פרטית, מאות פתיחות ביום מול עשר בבית. בגלל זה אני ממליץ על דגמים ייעודיים לאירוח ולא על מנעול ביתי רגיל, ההבדל במחיר קטן וההבדל באורך החיים גדול. גם השירות אחרי ההתקנה מותאם לקצב של עסק חי.',
 'katalog-ksafot':'עוד נקודה שחוזרת אצל לקוחות היא הביטוח. חברות ביטוח רבות דורשות כספת מעוגנת לתכולה מבוטחת כמו תכשיטים ומזומן, ולפעמים גם דרגת עמידות מסוימת. לפני קנייה שווה להרים טלפון לסוכן הביטוח, ואני כבר מתאים את הכספת והעיגון לדרישות שקיבלתם.',
 'katalog-mahzirei-delet':'מחזיר דלת מכוון נכון מרגישים מיד, הדלת נסגרת ברכות, בלי טריקה ובלי להישאר פתוחה. הכיוון תלוי במשקל הדלת, ברוח במעבר ובעונה, בחורף שמן המחזיר מתעבה והדלת מתנהגת אחרת. בכל התקנה שלי הכיוון כלול, וגם כיוון חוזר אחרי ההרצה הראשונה.',
 'katalog-parzol-adrichali':'פרזול הוא המקום שבו הכי קל לזהות חיסכון לא נכון. ידית זולה מתרופפת אחרי חצי שנה, ציר לא מתאים חורק ושוחק את הדלת, ומעצור פלסטיק נשבר בשבוע. ההפרש בין פריט בסיסי לפריט איכותי הוא עשרות שקלים, וההבדל בשטח מורגש כל יום.',
 'katalog-potchei-dlatot':'פותח דלת חשמלי הוא גם עניין של נוחות יומיומית וגם של בטיחות. בבניין מגורים הוא חוסך ירידה לדלת בכל צלצול, ובעסק הוא שולט מי נכנס ומתי. חשוב להתאים את הפותח לסוג המשקוף ולמשקל הדלת, התאמה לא נכונה מתבטאת בזמזום בלי פתיחה.',
 'katalog-yadiyot-bahala':'בביקורות של כיבוי אש ידית בהלה תקינה היא סעיף שחוזר שוב ושוב. עסק שנדרש לדלת חירום צריך ידית שנפתחת בלחיצה אחת גם בחושך וגם בלחץ של אנשים, בלי מפתח ובלי ידע מוקדם. אני מתקין את הידית ומוודא שהיא עומדת בדרישות של יועץ הבטיחות.',
}

def shell(slug,title,meta,h1,intro,main,ld):
    lds='<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>'
    html=f'''<!doctype html>
<html dir="rtl" lang="he">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="{BASE}/{slug}.html"><link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png"><link rel="icon" type="image/png" sizes="16x16" href="favicon-16.png"><link rel="icon" href="favicon.ico"><link rel="apple-touch-icon" href="apple-touch-icon.png">
{lds}
{style}
</head>
<body>
<div class="n6">
{ub}
{header}
  <nav class="bc" aria-label="פירורי לחם"><div class="wrap"><a href="index.html">בית</a><span aria-hidden="true">›</span><a href="katalog.html">קטלוג מוצרים</a><span aria-hidden="true">›</span><b>{h1}</b></div></nav>
  <section class="phero"><div class="wrap"><h1>{h1}</h1><p>{intro}</p></div></section>
{main}
{CTA}
{footer}
{flt}
{smob}
</div>
{js}
</body>
</html>'''
    open(f'/Users/s/niv-locksmith/{slug}.html','w',encoding='utf-8').write(html)

banned=["לסיכום","ראשית,","שנית","בנוסף לכך","יתרה מזאת","חשוב לציין","במסגרת","על מנת","כמו כן","יש לציין"]
for slug,d in CATS.items():
    def card(p):
        pi=PIDX.get(p["name"])
        if pi:
            return f'<a class="pcard" href="{pi["slug"]}.html"><span class="pcard__img"><img src="img/products/{pi["img"]}.jpg" alt="{p["name"]}" loading="lazy"></span><span class="tag">{p.get("tag","")}</span><b>{p["name"]}</b><p>{p["desc"]}</p><span class="ask">לעמוד המוצר ›</span></a>'
        return f'<div class="pcard"><span class="tag">{p.get("tag","")}</span><b>{p["name"]}</b><p>{p["desc"]}</p><a class="ask" href="tel:+972508307269">להתייעצות על הדגם ›</a></div>'
    cards="".join(card(p) for p in d["products"])
    revs="".join(f'<div class="revbox"><h3>{r["h"]}</h3><p>{r["t"]}</p><p class="src">{r["src"]}</p></div>' for r in d["reviews"])
    blocks="".join(f'<h2>{h}</h2><p>{t}</p>' for h,t in d["blocks"])
    faq="".join(f'<div class="faq__i"><button class="faq__q" aria-expanded="false" aria-controls="cf{i}">{q}<span class="s" aria-hidden="true">+</span></button><div class="faq__a" id="cf{i}">{a}</div></div>' for i,(q,a) in enumerate(d["faq"],1))
    main=f'''
  <div class="content"><p style="font-size:16.5px">{d["opening"]}</p></div>
  <section class="sec sec--sand" style="padding-top:30px"><div class="wrap">
    <div class="sh sh--c"><h2>הדגמים בקטלוג</h2><p>קטלוג להתרשמות והתייעצות. אני מתקין את כל המוצרים, המחיר נסגר בטלפון לפי הדלת שלכם.</p></div>
    <div class="pgrid">{cards}</div>
  </div></section>
  <div class="content">{blocks}
  <h2>מה אומרים על המותגים המובילים</h2>{revs}</div>
  {('<p style="max-width:900px;margin:0 auto 26px;padding:0 22px;font-size:16.5px;line-height:1.75">'+TOPUP[slug]+'</p>') if slug in TOPUP else ''}
  <section class="sec sec--sand"><div class="wrap"><div class="sh sh--c"><h2>שאלות על {d["h1"]}</h2></div><div class="faq">{faq}</div></div></section>'''
    ld={"@context":"https://schema.org","@graph":[
     {"@type":"Locksmith","@id":BASE+"/#business","name":"ניב המנעולן","telephone":"+972508307269","url":BASE+"/",
      "address":{"@type":"PostalAddress","addressLocality":"ירושלים","addressCountry":"IL"}},
     {"@type":"ItemList","name":d["h1"],"numberOfItems":len(d["products"]),
      "itemListElement":[{"@type":"ListItem","position":i+1,"item":{"@type":"Product","name":p["name"],"description":p["desc"]}} for i,p in enumerate(d["products"])]},
     {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in d["faq"]]},
     {"@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"בית","item":BASE+"/"},
      {"@type":"ListItem","position":2,"name":"קטלוג מוצרים","item":BASE+"/katalog.html"},
      {"@type":"ListItem","position":3,"name":d["h1"],"item":BASE+"/"+slug+".html"}]}]}
    shell(slug,d["title"],d["meta"],d["h1"],d["intro"],main,ld)
    s=open(f'/Users/s/niv-locksmith/{slug}.html',encoding='utf-8').read()
    t=re.sub(r'<script.*?</script>','',s,flags=re.S); t=re.sub(r'<style.*?</style>','',t,flags=re.S); t=re.sub(r'<[^>]+>',' ',t)
    bad=[w for w in banned if w in t]
    print(slug,len(t.split()),'words | banned:',bad or 'OK')
