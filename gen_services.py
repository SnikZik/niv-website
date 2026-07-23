# -*- coding: utf-8 -*-
import re,json,sys
sys.path.insert(0,'/Users/s/niv-locksmith')
from services_deep import DEEP,T

src=open('/Users/s/niv-locksmith/index.html',encoding='utf-8').read()
style=re.search(r'<style>.*?</style>',src,re.S).group(0)
ub=re.search(r'<div class="ub">.*?</div></div>',src,re.S).group(0)
header=re.search(r'<header class="hd">.*?</header>',src,re.S).group(0)
footer=re.search(r'<footer class="ft">.*?</footer>',src,re.S).group(0)
flt=re.search(r'<div class="float">.*?</div>\s*(?=<div class="smob">)',src,re.S).group(0)
smob=re.search(r'<div class="smob">.*?</div>\s*(?=</div>)',src,re.S).group(0)
js=re.search(r'<script>.*?</script>',src,re.S).group(0)
hero1=re.search(r'class="bighero__bg" src="(data:[^"]+)"',src).group(1)
hero2=re.search(r'src="(data:[^"]+)" alt="ניב, מנעולן בירושלים',src).group(1)

# service-page CSS (split hero with image + deep + reviews)
extra_css='''
/* ===== service page v2 ===== */
.n6 .bc{background:#fff;border-bottom:1px solid var(--line);font-size:13.5px;padding:10px 0}
.n6 .bc .wrap{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.n6 .bc a{color:var(--iron)} .n6 .bc a:hover{color:var(--red)} .n6 .bc b{color:var(--ink);font-weight:700}
.n6 .shero{background:linear-gradient(180deg,#EAF1F7,#FFFFFF);border-bottom:1px solid var(--line)}
.n6 .shero__in{display:grid;grid-template-columns:1.1fr .9fr;gap:44px;align-items:center;padding:44px 22px;max-width:1140px;margin-inline:auto}
.n6 .shero h1{font-size:36px;line-height:1.15;margin-bottom:12px}
.n6 .shero__sub{font-size:17px;color:var(--ink);line-height:1.65;margin-bottom:16px}
.n6 .shero__img img{border-radius:18px;box-shadow:var(--sh2);width:100%;height:100%;object-fit:cover;max-height:420px}
.n6 .shero .btnrow{margin-top:16px}
.n6 .shero .hchecks{margin-top:18px}
.n6 .updated{font-size:13.5px;color:var(--iron);margin-top:14px}
.n6 .defbox{background:var(--white);border:1px solid var(--line);border-inline-start:4px solid var(--red);border-radius:12px;padding:22px 24px;box-shadow:var(--sh)}
.n6 .defbox h2{font-size:22px;margin-bottom:8px}
.n6 .defbox p{margin:0;font-size:16.5px}
.n6 .deep h2{font-size:25px;margin:30px 0 10px}
.n6 .deep h2:first-of-type{margin-top:0}
.n6 .deep p{font-size:16.5px;line-height:1.7;margin-bottom:8px}
.n6 .probs--svc{grid-template-columns:1fr 1fr;margin-top:18px}
.n6 .steps2--svc{margin-top:18px}
.n6 .scards--rel{grid-template-columns:repeat(4,1fr)}
.n6 .sec--white .prose h2,.n6 .sec--white>.wrap>h2,.n6 .sec--sand>.wrap>h2,.n6 .sec--white>.wrap>.narrow>h2{font-size:26px;margin-bottom:8px}
.n6 .svcrev{display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:860px;margin:24px auto 0}
.n6 .svcrev .tcard{height:100%}
@media(max-width:900px){
  .n6 .shero__in{grid-template-columns:1fr;gap:22px;padding:22px 22px 30px}
  .n6 .shero h1{font-size:28px;margin-bottom:8px}
  .n6 .bc{padding:7px 0;font-size:12.5px}
  .n6 .shero .btnrow{margin-top:0}
  .n6 .shero .btnrow .btn--lg{padding:15px 20px}
  .n6 .shero__img{order:2}
  .n6 .probs--svc{grid-template-columns:1fr}
  .n6 .scards--rel{grid-template-columns:1fr 1fr}
  .n6 .svcrev{grid-template-columns:1fr}
}
/* availability line */
.n6 .avail{display:flex;align-items:center;gap:8px;font-weight:700;font-size:15px;color:var(--ink);margin-bottom:14px}
.n6 .avail .dot{width:10px;height:10px;border-radius:50%;background:#0A7536;box-shadow:0 0 0 3px rgba(10,117,54,.18);flex:none}
/* red price band */
.n6 .band2{background:var(--red);color:#fff;text-align:center;padding:30px 22px}
.n6 .band2 b{display:block;font-size:22px;margin-bottom:6px}
.n6 .band2 p{color:#F6DCD9;font-size:15.5px;margin:0 0 16px}
.n6 .band2 a{display:inline-flex;align-items:center;gap:9px;background:#fff;color:var(--red);font-weight:800;border-radius:12px;padding:14px 26px;font-size:16.5px}
.n6 .emerg .btnrow{margin-top:4px}
@media(max-width:560px){
  .n6 .band2 a{width:100%;justify-content:center;display:flex}
  .n6 .emerg .btnrow .btn{width:100%;justify-content:center}
  .n6 .about .btn{width:100%;justify-content:center;display:flex}
  .n6 .about__in{gap:20px}
  .n6 .about{padding:44px 0}
}
'''
style=style.replace('</style>', extra_css+'\n</style>')

PH='<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.3 1.8.6 2.6a2 2 0 0 1-.5 2.1L8 9.6a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.5c.8.3 1.7.5 2.6.6a2 2 0 0 1 1.7 2Z"/></svg>'
WA='<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-12.3 7.5L3 21l2-5.6A8.4 8.4 0 1 1 21 11.5Z"/></svg>'
CK='<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>'
WAURL='https://wa.me/972508307269?text=%D7%A9%D7%9C%D7%95%D7%9D%20%D7%A0%D7%99%D7%91'
BASE='https://snikzik.github.io/niv-website'
CAM='<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M4 8h3l2-3h6l2 3h3v12H4z"/><circle cx="12" cy="13" r="3.5"/></svg>'
SHIELD='<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5l-8-3Z"/><path d="m9 12 2 2 4-4"/></svg>'
COIN='<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M9 15V9h4a2 2 0 0 1 0 4H9"/></svg>'
HOMEI='<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M3 10.5 12 3l9 7.5M5 9.5V21h14V9.5"/></svg>'
HEART='<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M12 21C7 16.5 3 13.3 3 9.3A4.3 4.3 0 0 1 7.3 5c1.9 0 3.5 1 4.7 2.6C13.2 6 14.8 5 16.7 5A4.3 4.3 0 0 1 21 9.3c0 4-4 7.2-9 11.7Z"/></svg>'

S=json.load(open('/Users/s/niv-locksmith/services_data.json',encoding='utf-8'))
PHB='<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.3 1.8.6 2.6a2 2 0 0 1-.5 2.1L8 9.6a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.5c.8.3 1.7.5 2.6.6a2 2 0 0 1 1.7 2Z"/></svg>'
CALLA='<a href="tel:+972508307269">חייגו לניב 050-8307269</a>'
WAA='<a href="'+WAURL+'" target="_blank" rel="noopener">שלחו צילום עכשיו</a>'
ADV={
 'A':('purple',CAM,'שולחים צילום, מקבלים מחיר','צלמו את הדלת או המנעול, שלחו לי בוואטסאפ, ותוך כמה דקות תדעו בדיוק כמה זה עולה.',WAA),
 'B':('blue',PHB,'מי שעונה לטלפון הוא מי שמגיע','בלי מוקד, בלי קבלני משנה ובלי הפתעות. סוגרים איתי מחיר בשיחה, ואני זה שדופק בדלת.',CALLA),
 'C':('teal',SHIELD,'פותח בזהירות, בלי נזק','ברוב המקרים הדלת נשארת שלמה לגמרי. המטרה שלי שתיכנסו הביתה בלי להחליף כלום.',CALLA),
 'D':('amber',COIN,'המחיר נסגר בטלפון, לא בשטח','לפני שאני יוצא אתם יודעים בדיוק כמה זה עולה. מה שסוכם בשיחה הוא מה שמשולם בסוף.',CALLA),
 'E':('indigo',HOMEI,'מקומי שמכיר כל שכונה','אני עובד רק בירושלים והסביבה. מכיר את הדלתות של כל שכונה, ולכן מגיע מהר ומוכן.',CALLA),
 'F':('rose',HEART,'רוב הלקוחות מגיעים בהמלצה','שכן ממליץ לשכן, לקוח מביא לקוח. ככה אני עובד בירושלים כבר שנים, בלי פרסום רועש.',CALLA),
}
ADVMAP={'pritzat-dlatot':'C','tzilinder':'F','tikun-dlatot':'D','mamad':'C','ksafot':'F','manul-hacham':'A',
 'mahzirei-delet':'D','electromagnet':'E','yadiyot-bahala':'B','pladelet':'E','rav-bariach':'C','manulan-herum':'B',
 'tikun-mamad':'D','kivun-dlatot-pnim':'C','dlatot-hutz':'E','hatkanat-mamad':'B','hatkanat-ksafot':'F',
 'yadiot-ledelet':'D','mafteah-shavur':'C','hatkanat-manulim':'A'}
try:
    from services_new import NEW
    for k,v in NEW.items():
        dp=v.pop('deep'); S[k]=v; DEEP[k]=dp
except ImportError:
    pass

def schema(slug,d,dp):
    url=f'{BASE}/{slug}.html'
    biz={"@type":"Locksmith","@id":BASE+"/#business","name":"ניב המנעולן","telephone":"+972508307269",
     "url":BASE+"/", "image":BASE+"/logo.png","priceRange":"₪₪",
     "address":{"@type":"PostalAddress","addressLocality":"ירושלים","addressCountry":"IL"},
     "areaServed":[{"@type":"City","name":"ירושלים"},{"@type":"City","name":"גבעת זאב"},{"@type":"City","name":"מבשרת ציון"},{"@type":"City","name":"מעלה אדומים"}],
     "openingHoursSpecification":{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"00:00","closes":"23:59"}}
    svc={"@type":"Service","name":d["h1"],"serviceType":dp["svc_type"],"provider":{"@id":BASE+"/#business"},
     "areaServed":{"@type":"City","name":"ירושלים"},"url":url,"description":d["meta"]}
    faq={"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in d["faq"]]}
    bc={"@type":"BreadcrumbList","itemListElement":[
     {"@type":"ListItem","position":1,"name":"בית","item":BASE+"/"},
     {"@type":"ListItem","position":2,"name":"שירותים","item":BASE+"/#services"},
     {"@type":"ListItem","position":3,"name":d["h1"],"item":url}]}
    g={"@context":"https://schema.org","@graph":[biz,svc,faq,bc]}
    return '<script type="application/ld+json">'+json.dumps(g,ensure_ascii=False)+'</script>'

def page(slug,d):
    dp=DEEP[slug]
    checks="".join(f'<div class="hcheck">{CK}{c}</div>' for c in d["checks"])
    probs="".join(f'<div class="prob"><span class="prob__d" aria-hidden="true"></span><div><b>{t}</b><p>{p}</p></div></div>' for t,p in d["situations"])
    steps="".join(f'<div class="step2"><b>{t}</b><p>{p}</p></div>' for t,p in d["steps"])
    facts="".join(f'<li><b>{t}</b> — {p}</li>' for t,p in d["factors"])
    deep="".join(f'<h2>{h}</h2><p>{p}</p>' for h,p in dp["blocks"])
    trows="".join(f'<div class="prow"><span class="prow__s">{a}</span><span class="prow__p">{b}</span></div>' for a,b in dp["table"])
    faq="".join(f'<div class="faq__i"><button class="faq__q" aria-expanded="false" aria-controls="sf{i}">{q}<span class="s" aria-hidden="true">+</span></button><div class="faq__a" id="sf{i}">{a}</div></div>' for i,(q,a) in enumerate(d["faq"],1))
    rel="".join(f'<a class="scard" href="/{s2}.html"><h3>{t}</h3><p>{p}</p><span class="scard__l">{l} ›</span></a>' for s2,t,p,l in d["related"])
    revs="".join(f'<div class="tcard"><p class="tcard__q">{T[k][0]}</p><div class="tcard__w">{T[k][1]}, <span>{T[k][2]}</span></div></div>' for k in dp["reviews"])
    revcols='repeat(3,1fr)' if len(dp["reviews"])>=3 else '1fr 1fr'
    advk=ADVMAP.get(slug,'C'); ac,ai,at,ax,acta=ADV[advk]
    advb=f'<section class="adv adv--{ac}"><span class="ic">{ai}</span><b>{at}</b><p>{ax}</p>{acta}</section>' 
    main=f'''
  <nav class="bc" aria-label="פירורי לחם"><div class="wrap">
    <a href="/">בית</a><span aria-hidden="true">›</span><a href="/">שירותים</a><span aria-hidden="true">›</span><b>{d["h1"]}</b>
  </div></nav>
  <section class="shero"><div class="shero__in">
    <div>
      <h1>{d["h1"]}</h1>
      <p class="avail"><span class="dot" aria-hidden="true"></span>זמין עכשיו · עונה ישירות, בלי מוקד</p>
      <div class="btnrow">
        <a class="btn btn--call btn--lg" href="tel:+972508307269">{PH}חייגו לניב עכשיו</a>
        <a class="btn btn--wa btn--lg" href="{WAURL}" target="_blank" rel="noopener">{WA}שלחו צילום ב-WhatsApp</a>
      </div>
      <div class="pchip"><b>{d["price"]}</b><span>{d["price_note"]}</span></div>
      <p class="shero__sub" style="margin-top:14px">{d["sub"]}</p>
      <div class="hchecks">{checks}</div>
      <p class="updated">מאת ניב, מנעולן מוסמך · עודכן ביולי 2026</p>
    </div>
    <div class="shero__img"><img src="img/{slug}.jpg" alt="{dp['svc_type']} בירושלים, ניב המנעולן" loading="eager"></div>
  </div></section>
  <section class="sec sec--white"><div class="wrap narrow">
    <div class="defbox"><h2>{dp["def_h"]}</h2><p>{dp["def"]}</p></div>
  </div></section>
  <section class="sec sec--white" style="padding-top:0"><div class="wrap narrow">
    <h2>{d["h2_when"]}</h2>
    <div class="probs probs--svc">{probs}</div>
  </div></section>
  <section class="sec sec--sand"><div class="wrap narrow deep">{deep}</div></section>
  <section class="emerg">
    <h2>{d["cta_h"]}</h2>
    <p>אני זמין עכשיו. חייגו, תארו מה קרה, ותקבלו מחיר וזמן הגעה כבר בשיחה. בתוך ירושלים אני בדרך כלל אצלכם תוך כ-20 דקות.</p>
    <div class="btnrow" style="justify-content:center">
      <a class="btn btn--call btn--lg" href="tel:+972508307269">חייגו 050-8307269</a>
      <a class="btn btn--wa btn--lg" href="{WAURL}" target="_blank" rel="noopener">שלחו WhatsApp</a>
    </div>
  </section>
  <section class="sec sec--white"><div class="wrap narrow">
    <h2>איך זה עובד</h2>
    <div class="steps2 steps2--svc">{steps}</div>
  </div></section>
  <section class="sec sec--sand"><div class="wrap narrow">
    <h2 style="text-align:center">{dp["table_h"]}</h2>
    <div class="ptable" style="margin-top:22px">{trows}</div>
    <p class="pnote">מחירי ״החל מ-״. המחיר המדויק נסגר בטלפון לפני שאני יוצא.</p>
  </div></section>
  <section class="sec sec--white"><div class="wrap narrow prose">
    <h2>{d["h2_price"]}</h2>
    <p>{d["price_intro"]}</p>
    <ul>{facts}</ul>
    <p class="m">{d["price_close"]}</p>
  </div></section>
  {advb}
  <section class="about"><div class="wrap"><div class="about__in">
    <div class="about__img"><img src="{hero2}" alt="ניב, מנעולן בירושלים, עובד על מנגנון של דלת"></div>
    <div>
      <h2>מי מגיע אליכם</h2>
      <p>אני ניב, מנעולן שעובד בירושלים והסביבה. {d["about"]}</p>
      <p class="m">מגיע לכל שכונות ירושלים וגם לגבעת זאב, מבשרת ציון ומעלה אדומים.</p>
      <a class="btn btn--call" href="tel:+972508307269">חייגו 050-8307269</a>
    </div>
  </div></div></section>
  <section class="sec sec--white" style="background:#EFF6F1"><div class="wrap">
    <div class="sh sh--c"><h2>מה לקוחות סיפרו</h2></div>
    <div class="svcrev" style="grid-template-columns:{revcols}">{revs}</div>
    <p style="text-align:center;color:var(--iron);font-size:14px;margin-top:16px">ביקורות מלקוחות אמיתיים של ניב. עזרתי גם לכם? אשמח לביקורת ב-Google.</p>
  </div></section>
  <section class="band2">
    <b>{dp["table"][0][0]} {dp["table"][0][1]}</b>
    <p>המחיר נסגר בטלפון, לפני שאני יוצא. בלי הפתעות בשטח.</p>
    <a href="tel:+972508307269">{PH}חייגו לניב 050-8307269</a>
  </section>
  <section class="sec sec--sand"><div class="wrap">
    <div class="sh sh--c"><h2>{d["h2_faq"]}</h2></div>
    <div class="faq">{faq}</div>
  </div></section>
  <section class="sec sec--white"><div class="wrap">
    <div class="sh sh--c"><h2>שירותים קשורים</h2></div>
    <div class="scards scards--rel">{rel}</div>
  </div></section>
  <section class="sec sec--sand"><div class="wrap narrow" style="text-align:center">
    <h2 style="font-size:22px;margin-bottom:14px">{d["areas_h"]}</h2>
    <div style="margin:0 0 18px;border-radius:14px;overflow:hidden;box-shadow:var(--sh)"><iframe loading="lazy" title="אזור השירות של ניב המנעולן בירושלים" src="https://www.google.com/maps?q=%D7%99%D7%A8%D7%95%D7%A9%D7%9C%D7%99%D7%9D&output=embed&z=12" style="border:0;width:100%;height:300px;display:block"></iframe></div>
    <p style="color:var(--iron);font-size:15px;line-height:1.8">פסגת זאב · רמות · גילה · תלפיות · קטמון · בית הכרם · קריית יובל · הר חומה · ארנונה · בקעה · נווה יעקב · וגם גבעת זאב, מבשרת ציון ומעלה אדומים</p>
  </div></section>
  <section class="sec fcta" style="text-align:center;padding:52px 22px">
    <h2 style="font-size:28px;margin-bottom:10px">{d["cta_h"]}</h2>
    <p style="margin-bottom:22px;font-size:17px">חייגו, תארו מה קרה, ותקבלו מחיר וזמן הגעה כבר בשיחה.</p>
    <div class="btnrow" style="justify-content:center">
      <a class="btn btn--call btn--lg" href="tel:+972508307269">חייגו 050-8307269</a>
      <a class="btn btn--wa btn--lg" href="{WAURL}" target="_blank" rel="noopener">שלחו WhatsApp</a>
    </div>
  </section>'''
    ld=schema(slug,d,dp)
    return f'<!doctype html>\n<html dir="rtl" lang="he">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>{d["title"]}</title>\n<meta name="description" content="{d["meta"]}">\n<link rel="canonical" href="{BASE}/{slug}.html">\n{ld}\n{style}\n</head>\n<body>\n<div class="n6">\n{ub}\n{header}\n{main}\n{footer}\n{flt}\n{smob}\n</div>\n{js}\n</body>\n</html>'

banned=["לסיכום","ראשית","שנית","בנוסף לכך","יתרה מזאת","חשוב לציין","במסגרת","על מנת","כמו כן","יש לציין"]
DROP=[("פריצת דלתות בירושלים","/pritzat-dlatot.html"),("החלפת צילינדר בירושלים","/tzilinder.html"),
("תיקון דלתות בירושלים","/tikun-dlatot.html"),("פריצת דלת ממ״ד בירושלים","/mamad.html"),
("פריצת כספות בירושלים","/ksafot.html"),("התקנת מנעול חכם בירושלים","/manul-hacham.html"),
("התקנת מחזירי דלת","/mahzirei-delet.html"),("התקנת אלקטרומגנט","/electromagnet.html"),
("התקנת ידיות בהלה","/yadiyot-bahala.html"),("דלת פלדלת כולל משקוף","/pladelet.html"),
("החלפת מנעול רב בריח","/rav-bariach.html"),("מנעולן חירום בירושלים","/manulan-herum.html")]
FOOT=[("פריצת דלתות","/pritzat-dlatot.html"),("החלפת צילינדר","/tzilinder.html"),("תיקון דלתות","/tikun-dlatot.html"),
("פריצת דלת ממ״ד","/mamad.html"),("מנעול חכם","/manul-hacham.html"),("מחזירי דלת","/mahzirei-delet.html"),
("אלקטרומגנט","/electromagnet.html"),("ידיות בהלה","/yadiyot-bahala.html"),("דלת פלדלת + משקוף","/pladelet.html")]

import re as _re
for slug,d in S.items():
    html=page(slug,d)
    for txt,url in DROP: html=html.replace('<a href="#">'+txt+'</a>','<a href="'+url+'">'+txt+'</a>')
    for txt,url in FOOT: html=html.replace('<li><a href="#">'+txt+'</a></li>','<li><a href="'+url+'">'+txt+'</a></li>')
    bad=[w for w in banned if w in html]
    text=_re.sub(r'<script.*?</script>','',html,flags=_re.S)
    text=_re.sub(r'<style.*?</style>','',text,flags=_re.S)
    text=_re.sub(r'<[^>]+>',' ',text); words=len(text.split())
    open(f'/Users/s/niv-locksmith/{slug}.html','w',encoding='utf-8').write(html)
    print(f'{slug}: {words}w banned:{bad or "OK"}')
