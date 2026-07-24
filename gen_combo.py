# -*- coding: utf-8 -*-
# service × area combo pages engine (8 services × 31 areas)
import re,json,sys,os,hashlib,urllib.parse
sys.path.insert(0,'/Users/s/niv-locksmith')
from areas_data import AREAS

BASE='https://snikzik.github.io/niv-website'
WAURL='https://wa.me/972508307269?text=%D7%A9%D7%9C%D7%95%D7%9D%20%D7%A0%D7%99%D7%91'

src=open('/Users/s/niv-locksmith/manulan-rehavia.html',encoding='utf-8').read()
style=re.search(r'<style>.*?</style>',src,re.S).group(0)
ub=re.search(r'<div class="ub">.*?</div></div>',src,re.S).group(0)
header=re.search(r'<header class="hd">.*?</header>',src,re.S).group(0)
footer=re.search(r'<footer class="ft">.*?</footer>',src,re.S).group(0)
flt=re.search(r'<div class="float">.*?</div>\s*(?=<div class="smob">)',src,re.S).group(0)
smob=re.search(r'<div class="smob">.*?</div>\s*(?=</div>)',src,re.S).group(0)
js_all=re.findall(r'<script>.*?</script>',src,re.S)
js=[x for x in js_all if 'application/ld' not in x][-1]

BANKS={}
for i in (1,2,3):
    try: BANKS.update(json.load(open(f'/Users/s/niv-locksmith/bank_{i}.json',encoding='utf-8')))
    except FileNotFoundError: pass

SVCS=[("pritzat-dlatot","פריצת דלתות"),("tzilinder","החלפת צילינדר"),("tikun-dlatot","תיקון דלתות"),
("mamad","דלת ממ״ד"),("manul-hacham","מנעול חכם"),("mafteah-shavur","חילוץ מפתח שבור"),
("ksafot","פריצת כספות"),("manulan-herum","מנעולן חירום 24/7")]

STRIP={"pritzat-dlatot":["מנעולים מכניים","מנעולים חבויים אמריקאיים","מנעולים אלקטרומכניים","מנעול חכם Yale Linus L2"],
"tzilinder":["מנעולים מכניים","מנעולים חבויים אמריקאיים","מנעולים אלקטרומכניים","מנעולי פבלוק"],
"tikun-dlatot":["ידית מנוף AH200 על רוזטה עגולה","מחזיר דלת הידראולי DC140","ידיות TESA לדלתות פנים","מחזיר דלת הידראולי DC200"],
"mamad":["ידית AH200 על שלט Grade 4","מחזיר דלת הידראולי DC340","ידית מנוף AH200 על רוזטה עגולה","מנעולים מכניים"],
"manul-hacham":["מנעול חכם Yale Linus L2","ערכת Linus L2 + קודן חכם","ערכת Linus L2 + קודן טביעת אצבע","קודן חכם Yale"],
"mafteah-shavur":["מנעולים מכניים","מנעולים חבויים אמריקאיים","מנעול חכם Yale Linus L2","מנעולי פבלוק"],
"ksafot":["כספת ביתית קטנה","כספת ביתית בינונית","כספת גבוהה","כספת High Security ביתית"],
"manulan-herum":["מנעולים מכניים","מנעול חכם Yale Linus L2","כספת ביתית קטנה","מחזיר דלת הידראולי DC140"]}
PIDX=json.load(open('/Users/s/niv-locksmith/products_index.json',encoding='utf-8'))

T={"yosi":("נתקעתי בלילה מחוץ לדירה עם הילדים. ניב ענה מיד, הגיע מהר ופתח בלי שום נזק. מציל.","יוסי","פסגת זאב"),
"oren":("החליף לי צילינדר אחרי שאיבדתי מפתחות. מחיר כמו שנאמר בטלפון, עבודה נקייה.","אורן","קטמון"),
"moshe":("הדלת של הממ״ד נתקעה, הגיע באותו יום וסידר. שירות אמין בלי סיפורים.","משה","רמות"),
"hila":("סגר לי מחיר בטלפון והגיע תוך רבע שעה. פתח את הדלת בשתי דקות. מומלץ.","הילה","גילה"),
"meital":("אדיב, מקצועי, ולא ניסה למכור לי כלום מעבר. ככה שירות צריך להיראות.","מיטל","בית שמש")}
REVROT=[["oren","moshe"],["yosi","hila"],["meital","oren"],["moshe","yosi"],["hila","meital"]]

ADV=[('linear-gradient(135deg,#3B1273,#6D28D9)','שולחים צילום, מקבלים מחיר','צלמו את הדלת או המנעול, שלחו בוואטסאפ, ותוך דקות יש מחיר סגור.',WAURL,'שלחו צילום עכשיו'),
('linear-gradient(135deg,#0C4A6E,#0369A1)','בלי מוקדנים, מדברים ישר איתי','מי שעונה לטלפון הוא מי שמגיע אליכם, עם הציוד ועם מחיר סגור.','tel:+972508307269','חייגו 050-8307269'),
('linear-gradient(135deg,#134E4A,#0F766E)','פותח בלי נזק לדלת','שיטות פתיחה עדינות, הדלת נשארת שלמה ברוב המקרים.','tel:+972508307269','דברו איתי'),
('linear-gradient(135deg,#78350F,#B45309)','המחיר נסגר בטלפון, לא בשטח','מה שסיכמנו בשיחה זה מה שתשלמו, בלי הפתעות.','tel:+972508307269','קבלו מחיר עכשיו'),
('linear-gradient(135deg,#312E81,#4338CA)','מנעולן מקומי בירושלים','מכיר כל שכונה וכל סוג דלת בעיר, ולכן מגיע מהר ועובד מדויק.','tel:+972508307269','חייגו עכשיו')]
CAM='<span class="ic"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M4 8h3l2-3h6l2 3h3v12H4z"/><circle cx="12" cy="13" r="3.5"/></svg></span>'

METAS={
 "pritzat-dlatot":["פריצת דלתות ב{A} 24/7. ניב מגיע תוך {E}, פותח בזהירות בלי נזק, מחיר סגור בטלפון מ-300₪. חייגו 050-8307269 עכשיו.",
 "ננעלתם ב{A}? פריצת דלת מקצועית תוך {E}, בלי נזק לדלת ובלי הפתעות במחיר. מ-300₪, סגור מראש בטלפון. חייגו 050-8307269.",
 "פריצת דלתות ב{A} עם מנעולן מקומי. הגעה תוך {E} ביום ובלילה, פתיחה עדינה ומחיר שנסגר בשיחה מ-300₪. חייגו 050-8307269."],
 "tzilinder":["החלפת צילינדר ב{A} תוך {E}. התאמת צילינדר רגיל או מוגן, עבודה נקייה ומחיר סגור בטלפון מ-300₪. חייגו 050-8307269.",
 "צריכים החלפת צילינדר ב{A}? ניב מגיע תוך {E} עם מבחר צילינדרים, מרכיב ומוסר מפתחות. מ-300₪ סגור מראש. חייגו 050-8307269.",
 "החלפת צילינדר ב{A}, גם באותו יום. צילינדר מוגן או רגיל לכל דלת, מחיר בטלפון מ-300₪ בלי תוספות. חייגו 050-8307269."],
 "tikun-dlatot":["תיקון דלתות ב{A} תוך {E}. צירים, כיוון, ידיות ומנגנונים, מחיר סגור בטלפון מ-350₪ בלי הפתעות. חייגו 050-8307269.",
 "דלת לא נסגרת ב{A}? ניב מתקן צירים, מנגנונים ומשקופים תוך {E}, במחיר שנסגר מראש מ-350₪. חייגו 050-8307269 עכשיו.",
 "תיקון דלת ב{A} עם מנעולן מקומי. אבחון מהיר, תיקון במקום ברוב המקרים, מ-350₪ סגור בטלפון. חייגו 050-8307269."],
 "mamad":["דלת ממ״ד תקועה ב{A}? תיקון מ-350₪ והתקנה מ-650₪, הגעה תוך {E} ומחיר סגור בטלפון. חייגו 050-8307269 לניב.",
 "טיפול בדלת ממ״ד ב{A}, כיוון, תיקון והתקנה. ניב מגיע תוך {E} עם הציוד המתאים, מחיר סגור מראש. חייגו 050-8307269.",
 "דלת ממ״ד ב{A} שלא נסגרת או חורקת? תיקון מקצועי מ-350₪, הגעה תוך {E}, מחיר בטלפון. חייגו 050-8307269."],
 "manul-hacham":["התקנת מנעול חכם ב{A} מ-1,499₪ כולל התקנה והדרכה. קוד, טביעת אצבע או אפליקציה. תיאום מהיר, ניב 050-8307269.",
 "מנעול חכם ב{A}? התאמה לדלת שלכם, התקנה מקצועית והדרכה מלאה, מ-1,499₪ הכל כלול. חייגו 050-8307269 לפרטים.",
 "רוצים להיכנס הביתה ב{A} בלי מפתח? מנעול חכם מותקן ומוגדר מ-1,499₪, כולל גיבוי לכל תרחיש. ניב 050-8307269."],
 "mafteah-shavur":["מפתח נשבר במנעול ב{A}? חילוץ עדין תוך {E} בלי נזק לצילינדר, מ-300₪ סגור בטלפון. חייגו 050-8307269 לניב.",
 "חילוץ מפתח שבור ב{A} ביום ובלילה. ניב מגיע תוך {E} עם כלים ייעודיים, המחיר נסגר בשיחה מ-300₪. חייגו 050-8307269.",
 "נשאר לכם חצי מפתח ביד ב{A}? חילוץ מקצועי מהצילינדר תוך {E}, מ-300₪ בלי הפתעות. חייגו 050-8307269."],
 "ksafot":["פריצת כספות ב{A} בלי נזק לתכולה. הגעה תוך {E}, מחיר לפי סוג הכספת נסגר בטלפון. כספת חדשה מ-499₪. ניב 050-8307269.",
 "כספת לא נפתחת ב{A}? קוד שנשכח או סוללה שמתה, ניב פותח בזהירות תוך {E}. מחיר סגור בשיחה. חייגו 050-8307269.",
 "פריצת כספת ב{A} עם מנעולן מקומי. פתיחה עדינה, אספקת כספת חדשה מ-499₪ כולל התקנה. חייגו 050-8307269 עכשיו."],
 "manulan-herum":["מנעולן חירום ב{A} 24/7. ניב מגיע תוך {E} בכל שעה, פותח בלי נזק ומחיר סגור בטלפון מ-300₪. חייגו 050-8307269.",
 "נתקעתם בחוץ ב{A} באמצע הלילה? מנעולן חירום אמיתי, בלי מוקד, הגעה תוך {E} ומחיר מראש. חייגו 050-8307269.",
 "מנעולן חירום ב{A} שעונה בעצמו. זמין יום ולילה, גם בשבתות וחגים, מ-300₪ סגור בשיחה. ניב 050-8307269."]}

TITLES=["{S} ב{A}, הגעה {E}, מחיר סגור מראש | ניב המנעולן",
"{S} ב{A} עם מנעולן מקומי זמין 24/7 | ניב המנעולן",
"{S} ב{A}, שירות מהיר במחיר סגור | ניב המנעולן ירושלים"]

def pick(lst,seed,salt=''):
    return lst[int(hashlib.md5((seed+salt).encode()).hexdigest(),16)%len(lst)]
def pidx(n,seed,salt=''):
    return int(hashlib.md5((seed+salt).encode()).hexdigest(),16)%n

def build(ai,area_slug,d,si,svc_key,svc_name,premium=frozenset()):
    short=area_slug.replace('manulan-','')
    slug=f'{svc_key}-{short}'
    if slug in premium: return slug,None
    B=BANKS[svc_key]
    A=d['b']; E=d['eta']
    def F(s): return s.replace('{AREA}',A).replace('{ETA}',E)
    seed=slug
    intro=F(pick(B['intro'],seed,'i'))
    body_a=F(pick(B['body_a'],seed,'a'))
    body_b=F(pick(B['body_b'],seed,'b'))
    price=F(pick(B['price'],seed,'p'))
    night=F(pick(B['night'],seed,'n'))
    loc_h,loc_t=d['local'][si%len(d['local'])]
    local=f'<h2>ההיכרות שלי עם {A}</h2><p>{loc_t}</p>'
    fq=B['faq']; start=pidx(len(fq),seed,'f')
    faqs=[(F(q),F(a)) for q,a in (fq[(start+k)%len(fq)] for k in range(5))]
    faq_html="".join(f'<div class="faq__i"><button class="faq__q" aria-expanded="false" aria-controls="cf{j}">{q}<span class="s" aria-hidden="true">+</span></button><div class="faq__a" id="cf{j}">{a}</div></div>' for j,(q,a) in enumerate(faqs,1))
    svc_links="".join(f'<a href="{s2}-{short}.html">{t2} ב{A}</a>' for s2,t2 in SVCS if s2!=svc_key)
    near="".join(f'<a href="{s2}.html">מנעולן ב{n}</a>' for s2,n in d['nearby'])
    revs=REVROT[(ai+si)%5]
    revh="".join(f'<div class="tcard"><p class="tcard__q">{T[k][0]}</p><div class="tcard__w">{T[k][1]}, <span>{T[k][2]}</span></div></div>' for k in revs)
    mapq=d.get('mapq',d['name']+' ירושלים')
    mapu='https://www.google.com/maps?q='+urllib.parse.quote(mapq)+'&output=embed&z=14'
    title=pick(TITLES,seed,'t').replace('{S}',svc_name).replace('{A}',A).replace('{E}',E)
    meta=pick(METAS[svc_key],seed,'m').replace('{A}',A).replace('{E}',E)
    strip_cards=''
    for nname in STRIP[svc_key]:
        p=PIDX.get(nname)
        if p: strip_cards+=f'<a class="pcard" href="{p["slug"]}.html"><span class="pcard__img"><img src="img/products/{p["img"]}.jpg" alt="{nname}" loading="lazy"></span><b>{nname}</b><span class="ask">לעמוד המוצר ›</span></a>'
    g,bt,bx,bhref,bcta=ADV[(ai+si)%5]
    tb=' target="_blank" rel="noopener"' if 'wa.me' in bhref else ''
    adv=f'<section class="adv" style="background:{g}">{CAM}<b>{bt}</b><p>{bx}</p><a href="{bhref}"{tb}>{bcta}</a></section>'
    faq_ld=[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',a)}} for q,a in faqs]
    graph=[{"@type":"Locksmith","@id":BASE+"/#business","name":"ניב המנעולן","telephone":"+972508307269","url":BASE+"/",
      "address":{"@type":"PostalAddress","addressLocality":"ירושלים","addressCountry":"IL"}},
     {"@type":"Service","name":f'{svc_name} ב{A}',"serviceType":svc_name,
      "provider":{"@id":BASE+"/#business"},"areaServed":{"@type":"Place","name":f'{A}, ירושלים'},
      "url":f'{BASE}/{slug}.html'},
     {"@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"בית","item":BASE+"/"},
      {"@type":"ListItem","position":2,"name":"אזורי שירות","item":BASE+"/azorei-sherut.html"},
      {"@type":"ListItem","position":3,"name":f'מנעולן ב{A}',"item":f'{BASE}/{area_slug}.html'},
      {"@type":"ListItem","position":4,"name":f'{svc_name} ב{A}',"item":f'{BASE}/{slug}.html'}]},
     {"@type":"FAQPage","mainEntity":faq_ld}]
    ld='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@graph":graph},ensure_ascii=False)+'</script>'
    main=f'''
  <nav class="bc" aria-label="פירורי לחם"><div class="wrap"><a href="index.html">בית</a><span aria-hidden="true">›</span><a href="azorei-sherut.html">אזורי שירות</a><span aria-hidden="true">›</span><a href="{area_slug}.html">מנעולן ב{A}</a><span aria-hidden="true">›</span><b>{svc_name} ב{A}</b></div></nav>
  <section class="ahero2"><div class="wrap">
    <span class="k">{svc_name} · {A} · הגעה {E}</span>
    <h1>{svc_name} ב{A}</h1>
    <p class="lead">{pick(["מנעולן מקומי, מחיר שנסגר בטלפון והגעה מהירה לכל רחוב ב"+A+".","שירות מקצועי ב"+A+" והסביבה, בלי מוקדנים ובלי הפתעות במחיר.","זמין עכשיו ל"+A+", עם מחיר סגור מראש ועבודה נקייה."],seed,'l')}</p>
    <div class="btnrow"><a class="btn btn--call btn--lg" href="tel:+972508307269">חייגו 050-8307269</a>
    <a class="btn btn--wa btn--lg" href="{WAURL}" target="_blank" rel="noopener">שלחו WhatsApp</a></div>
  </div></section>
  <section class="sec sec--white"><div class="wrap narrow content">
    {intro}
    {body_a}
  </div></section>
  <section class="sec sec--white" style="background:#F6F3FB"><div class="wrap"><div class="sh sh--c"><h2>מהקטלוג שלי</h2><p>עם ייעוץ והתקנה. המחיר נסגר בטלפון.</p></div><div class="pgrid" style="grid-template-columns:repeat(4,1fr)">{strip_cards}</div></div></section>
  <section class="sec sec--white"><div class="wrap narrow content">
    {local}
    {body_b}
  </div></section>
  {adv}
  <section class="sec sec--white"><div class="wrap narrow content">
    {price}
    {night}
  </div></section>
  <section class="sec sec--sand"><div class="wrap">
    <div class="sh sh--c"><h2>מה לקוחות מספרים</h2></div>
    <div class="tgrid" style="grid-template-columns:repeat(2,1fr);max-width:760px;margin-inline:auto">{revh}</div>
  </div></section>
  <section class="sec sec--sand"><div class="wrap">
    <div class="sh sh--c"><h2>שאלות על {svc_name} ב{A}</h2></div>
    <div class="faq">{faq_html}</div>
  </div></section>
  <section class="sec sec--white"><div class="wrap">
    <h2 style="font-size:24px">עוד שירותים ב{A}</h2>
    <div class="svclinks">{svc_links}</div>
    <h2 style="font-size:24px;margin-top:26px">אזור השירות</h2>
    <div style="margin:12px 0 18px;border-radius:14px;overflow:hidden;box-shadow:var(--sh)"><iframe loading="lazy" title="{svc_name} ב{A}, אזור שירות" src="{mapu}" style="border:0;width:100%;height:300px;display:block"></iframe></div>
    <div class="nearby">{near}</div>
  </div></section>
  <section class="sec fcta" style="text-align:center;padding:50px 22px">
    <h2 style="font-size:27px;margin-bottom:10px">צריכים {svc_name} ב{A}?</h2>
    <p style="margin-bottom:22px;font-size:17px">חייגו, תארו מה קרה, ותקבלו מחיר וזמן הגעה כבר בשיחה.</p>
    <div class="btnrow" style="justify-content:center">
      <a class="btn btn--call btn--lg" href="tel:+972508307269">חייגו 050-8307269</a>
      <a class="btn btn--wa btn--lg" href="{WAURL}" target="_blank" rel="noopener">שלחו WhatsApp</a>
    </div>
  </section>'''
    html=f'<!doctype html>\n<html dir="rtl" lang="he">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>{title}</title>\n<meta name="description" content="{meta}">\n<link rel="canonical" href="{BASE}/{slug}.html"><link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png"><link rel="icon" type="image/png" sizes="16x16" href="favicon-16.png"><link rel="icon" href="favicon.ico"><link rel="apple-touch-icon" href="apple-touch-icon.png">\n{ld}\n{style}\n</head>\n<body>\n<div class="n6">\n{ub}\n{header}\n{main}\n{footer}\n{flt}\n{smob}\n</div>\n{js}\n</body>\n</html>'
    return slug,html

if __name__=='__main__':
    premium=frozenset(sys.argv[1].split(',')) if len(sys.argv)>1 else frozenset()
    banned=["לסיכום","ראשית,","שנית,","בנוסף לכך","יתרה מזאת","חשוב לציין","במסגרת","על מנת","כמו כן","יש לציין","—","–"]
    n=0;probs=0
    items=AREAS.items() if isinstance(AREAS,dict) else [(a['slug'],a) for a in AREAS]
    for ai,(area_slug,d) in enumerate(items):
        for si,(svc_key,svc_name) in enumerate(SVCS):
            slug,html=build(ai,area_slug,d,si,svc_key,svc_name,premium)
            if html is None: continue
            bad=[w for w in banned if w in html]
            t=re.sub(r'<script.*?</script>','',html,flags=re.S); t=re.sub(r'<style.*?</style>','',t,flags=re.S); t=re.sub(r'<[^>]+>',' ',t)
            wc=len(t.split())
            if bad or wc<1100: probs+=1; print('PROB',slug,wc,bad)
            open(f'/Users/s/niv-locksmith/{slug}.html','w',encoding='utf-8').write(html)
            n+=1
    print('combo pages:',n,'problems:',probs)
