# -*- coding: utf-8 -*-
import re,json,sys

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
BASE='https://snikzik.github.io/niv-website'
WAURL='https://wa.me/972508307269?text=%D7%A9%D7%9C%D7%95%D7%9D%20%D7%A0%D7%99%D7%91'
PH='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.3 1.8.6 2.6a2 2 0 0 1-.5 2.1L8 9.6a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.5c.8.3 1.7.5 2.6.6a2 2 0 0 1 1.7 2Z"/></svg>'

art_css='''
/* ===== article page ===== */
.n6 .bc{background:#fff;border-bottom:1px solid var(--line);font-size:13.5px;padding:8px 0}
.n6 .bc .wrap{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.n6 .bc a{color:var(--iron)} .n6 .bc b{color:var(--ink);font-weight:700}
.n6 .ahero{background:linear-gradient(180deg,#EAF1F7,#fff);padding:34px 0 26px;border-bottom:1px solid var(--line)}
.n6 .ahero .k{display:inline-block;background:#fff;border:1px solid var(--line);border-radius:999px;color:var(--red);font-weight:800;font-size:13px;padding:5px 14px;margin-bottom:14px}
.n6 .ahero h1{font-size:34px;line-height:1.2;max-width:760px;margin-bottom:12px}
.n6 .ahero .lead{font-size:18px;color:var(--iron);max-width:700px;line-height:1.6}
.n6 .abyline{display:flex;align-items:center;gap:12px;margin-top:18px;font-size:14px;color:var(--iron)}
.n6 .abyline img{width:42px;height:42px;border-radius:50%;object-fit:cover}
.n6 .abyline b{color:var(--ink);display:block;font-size:14.5px}
.n6 .art{max-width:720px;margin-inline:auto;padding:34px 22px 10px}
.n6 .art h2{font-size:25px;margin:32px 0 10px}
.n6 .art h2:first-child{margin-top:0}
.n6 .art h3{font-size:19px;margin:22px 0 8px}
.n6 .art p{font-size:17px;line-height:1.75;margin-bottom:14px}
.n6 .art ul,.n6 .art ol{margin:0 0 16px;padding-inline-start:22px}
.n6 .art li{font-size:16.5px;line-height:1.7;margin-bottom:7px}
.n6 .art a{color:var(--red);font-weight:700;text-decoration:underline;text-underline-offset:3px}
.n6 .art .tip{background:var(--sand);border-inline-start:4px solid var(--red);border-radius:10px;padding:16px 18px;margin:20px 0;font-size:16px}
.n6 .art .tip b{color:var(--ink)}
.n6 .artimg{margin:22px 0;border-radius:14px;overflow:hidden;box-shadow:var(--sh)}
.n6 .artcta{background:var(--ink);color:#fff;border-radius:16px;padding:26px 24px;text-align:center;margin:30px 0}
.n6 .artcta b{display:block;font-size:20px;margin-bottom:6px}
.n6 .artcta p{color:#D8E2E8;font-size:15px;margin:0 0 16px;line-height:1.6}
.n6 .artcta a{display:inline-flex;align-items:center;gap:8px;background:var(--red);color:#fff;font-weight:800;border-radius:12px;padding:13px 24px;font-size:16px;text-decoration:none}
.n6 .relarts{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
@media(max-width:900px){
  .n6 .ahero h1{font-size:27px}
  .n6 .relarts{grid-template-columns:1fr}
  .n6 .artcta a{width:100%;justify-content:center;display:flex}
}
'''
style=style.replace('</style>',art_css+'\n</style>')


PIDX=json.load(open('/Users/s/niv-locksmith/products_index.json',encoding='utf-8'))
ART_STRIPS={
 'delet-nitreka':('צילינדרים ומנעולים מהקטלוג',['מנעולים מכניים','מנעולים חבויים אמריקאיים','מנעול חכם Yale Linus L2','מנעולים אלקטרומכניים']),
 'tzilinder-matay':('צילינדרים ומנעולים מהקטלוג',['מנעולים מכניים','מנעולים חבויים אמריקאיים','מנעולים אלקטרומכניים','מנעול חכם Yale Linus L2']),
 'kama-ole-manulan':('מהקטלוג שלי, מחיר סגור בטלפון',['מנעולים מכניים','כספת ביתית קטנה','מנעול חכם Yale Linus L2','מחזיר דלת הידראולי DC140']),
 'tzilinder-mugan-mul-ragil':('מנעולים וצילינדרים מהקטלוג',['מנעולים מכניים','מנעולים חבויים אמריקאיים','מנעולים אלקטרומכניים','מנעולי פבלוק']),
 'manul-hacham-madrich':('מנעולים חכמים מהקטלוג',['מנעול חכם Yale Linus L2','ערכת Linus L2 + קודן חכם','ערכת Linus L2 + קודן טביעת אצבע','קודן חכם Yale']),
 'mamad-takua':('פרזול ופתרונות לדלתות כבדות',['ידית AH200 על שלט Grade 4','מחזיר דלת הידראולי DC340','ידית מנוף AH200 על רוזטה עגולה','מנעולים מכניים']),
 'checklist-maavar-dira':('שדרוגים נפוצים במעבר דירה',['מנעולים מכניים','מנעול חכם Yale Linus L2','כספת ביתית קטנה','מנעולים חבויים אמריקאיים']),
 'manulan-oketz':('מוצרים שאני מתקין במחיר סגור',['מנעולים מכניים','מנעול חכם Yale Linus L2','כספת ביתית בינונית','מחזיר דלת הידראולי DC140']),
 'rav-bariach-kashe':('פרזול ומנעולים מהקטלוג',['מנעולים מכניים','ידית מנוף AH200 על רוזטה עגולה','מנעולים חבויים אמריקאיים','מחזיר דלת הידראולי DC200']),
 'delet-lo-nisgeret':('מחזירים ופרזול מהקטלוג',['מחזיר דלת הידראולי DC140','מחזיר דלת הידראולי DC200','ידית מנוף AH200 על רוזטה עגולה','ידיות TESA לדלתות פנים']),
}
ADV_ROT=[
 ('linear-gradient(135deg,#3B1273,#6D28D9)','שולחים צילום, מקבלים מחיר','צלמו את הדלת או המנעול, שלחו לי בוואטסאפ, ותוך כמה דקות תדעו בדיוק כמה זה עולה. עוד לפני שיצאתי אליכם.','שלחו צילום עכשיו'),
 ('linear-gradient(135deg,#0C4A6E,#0369A1)','בלי מוקדנים, מדברים ישר איתי','אין מוקד ואין תיווך. מי שעונה לטלפון הוא מי שמגיע אליכם, עם הציוד ועם המחיר שנסגר בשיחה.','חייגו 050-8307269'),
 ('linear-gradient(135deg,#134E4A,#0F766E)','פותח בלי נזק לדלת','כלי עבודה מקצועיים ושיטות פתיחה עדינות. הדלת נשארת שלמה והמנעול ברוב המקרים ממשיך לעבוד.','דברו איתי'),
 ('linear-gradient(135deg,#78350F,#B45309)','המחיר נסגר בטלפון, לא בשטח','מה שסיכמנו בשיחה זה מה שתשלמו. בלי תוספות מפתיעות ובלי ״נראה כשאגיע״.','קבלו מחיר עכשיו'),
 ('linear-gradient(135deg,#312E81,#4338CA)','מנעולן מקומי, תוך 20 דקות אצלכם','אני עובד רק בירושלים והסביבה, ולכן מגיע מהר ומכיר כל סוג דלת בעיר.','חייגו עכשיו'),
]
CAM_IC='<span class="ic"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M4 8h3l2-3h6l2 3h3v12H4z"/><circle cx="12" cy="13" r="3.5"/></svg></span>'
def art_strip(slug,idx):
    if slug not in ART_STRIPS: return ''
    head,names=ART_STRIPS[slug]
    cards=''
    for n in names:
        p=PIDX.get(n)
        if not p: continue
        cards+=f'<a class="pcard" href="{p["slug"]}.html"><span class="pcard__img"><img src="img/products/{p["img"]}.jpg" alt="{n}" loading="lazy"></span><b>{n}</b><span class="ask">לעמוד המוצר ›</span></a>'
    g,btitle,btext,bcta=ADV_ROT[idx%len(ADV_ROT)]
    href='https://wa.me/972508307269?text=%D7%A9%D7%9C%D7%95%D7%9D%20%D7%A0%D7%99%D7%91' if idx%len(ADV_ROT) in (0,2) else 'tel:+972508307269'
    tb=' target="_blank" rel="noopener"' if 'wa.me' in href else ''
    adv=f'<section class="adv" style="background:{g}">{CAM_IC}<b>{btitle}</b><p>{btext}</p><a href="{href}"{tb}>{bcta}</a></section>'
    strip=f'<section class="sec sec--white" style="background:#F6F3FB"><div class="wrap"><div class="sh sh--c"><h2>{head}</h2><p>מהקטלוג שלי, עם ייעוץ והתקנה. המחיר נסגר בטלפון.</p></div><div class="pgrid" style="grid-template-columns:repeat(4,1fr)">{cards}</div></div></section>'
    return strip+adv

def article(a,ai=0):
    body_html=a["body"]
    faq_ld=[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":ans}} for q,ans in a.get("faq",[])]
    graph=[
     {"@type":"Locksmith","@id":BASE+"/#business","name":"ניב המנעולן","telephone":"+972508307269","url":BASE+"/",
      "address":{"@type":"PostalAddress","addressLocality":"ירושלים","addressCountry":"IL"}},
     {"@type":"Article","headline":a["h1"],"description":a["meta"],"inLanguage":"he",
      "author":{"@type":"Person","name":"ניב","jobTitle":"מנעולן","worksFor":{"@id":BASE+"/#business"}},
      "publisher":{"@id":BASE+"/#business"},
      "datePublished":a["date"],"dateModified":a["date"],
      "mainEntityOfPage":BASE+"/"+a["slug"]+".html"},
     {"@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"בית","item":BASE+"/"},
      {"@type":"ListItem","position":2,"name":"מדריכים","item":BASE+"/#guides"},
      {"@type":"ListItem","position":3,"name":a["h1"],"item":BASE+"/"+a["slug"]+".html"}]}
    ]
    if faq_ld: graph.append({"@type":"FAQPage","mainEntity":faq_ld})
    ld='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@graph":graph},ensure_ascii=False)+'</script>'
    rel="".join(f'<div class="bpost"><div class="k">{k}</div><h3><a href="{s}.html">{t}</a></h3><p>{p}</p><a class="l" href="{s}.html">לקריאה ›</a></div>' for s,k,t,p in a["related_articles"])
    faq_html="".join(f'<div class="faq__i"><button class="faq__q" aria-expanded="false" aria-controls="af{i}">{q}<span class="s" aria-hidden="true">+</span></button><div class="faq__a" id="af{i}">{ans}</div></div>' for i,(q,ans) in enumerate(a.get("faq",[]),1))
    faq_sec=f'<section class="sec sec--sand"><div class="wrap"><div class="sh sh--c"><h2>שאלות נפוצות</h2></div><div class="faq">{faq_html}</div></div></section>' if faq_html else ''
    main=f'''
  <nav class="bc" aria-label="פירורי לחם"><div class="wrap">
    <a href="index.html">בית</a><span aria-hidden="true">›</span><a href="madrichim.html">מדריכים</a><span aria-hidden="true">›</span><b>{a["h1"]}</b>
  </div></nav>
  <section class="ahero"><div class="wrap">
    <span class="k">{a["cat"]}</span>
    <h1>{a["h1"]}</h1>
    <p class="lead">{a["lead"]}</p>
    <div class="abyline">
      <img src="{hero2}" alt="">
      <div><b>ניב, מנעולן בירושלים</b>עודכן {a["date_he"]} · קריאה של {a["mins"]} דקות</div>
    </div>
  </div></section>
  <article class="art">
    {body_html}
  </article>
  {faq_sec}
  {art_strip(a['slug'],ai)}
  <section class="sec sec--white"><div class="wrap">
    <div class="sh"><h2>עוד מדריכים</h2></div>
    <div class="bgrid relarts">{rel}</div>
  </div></section>
  <section class="sec fcta" style="text-align:center;padding:50px 22px">
    <h2 style="font-size:27px;margin-bottom:10px">צריכים מנעולן בירושלים?</h2>
    <p style="margin-bottom:22px;font-size:17px">חייגו, תארו מה קרה, ותקבלו מחיר וזמן הגעה כבר בשיחה.</p>
    <div class="btnrow" style="justify-content:center">
      <a class="btn btn--call btn--lg" href="tel:+972508307269">חייגו 050-8307269</a>
      <a class="btn btn--wa btn--lg" href="{WAURL}" target="_blank" rel="noopener">שלחו WhatsApp</a>
    </div>
  </section>'''
    html=f'<!doctype html>\n<html dir="rtl" lang="he">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>{a["title"]}</title>\n<meta name="description" content="{a["meta"]}">\n<link rel="canonical" href="{BASE}/{a["slug"]}.html">\n{ld}\n{style}\n</head>\n<body>\n<div class="n6">\n{ub}\n{header}\n{main}\n{footer}\n{flt}\n{smob}\n</div>\n{js}\n</body>\n</html>'
    html=html.replace('__HERO1__',hero1).replace('__PH__',PH)
    return html

sys.path.insert(0,'/Users/s/niv-locksmith')
from articles_data import ARTICLES
banned=["לסיכום","ראשית","שנית","בנוסף לכך","יתרה מזאת","חשוב לציין","במסגרת","על מנת","כמו כן","יש לציין"]
for ai,a in enumerate(ARTICLES):
    html=article(a,ai)
    bad=[w for w in banned if w in html]
    t=re.sub(r'<script.*?</script>','',html,flags=re.S); t=re.sub(r'<style.*?</style>','',t,flags=re.S); t=re.sub(r'<[^>]+>',' ',t)
    open('/Users/s/niv-locksmith/'+a["slug"]+'.html','w',encoding='utf-8').write(html)
    print(a["slug"],':',len(t.split()),'words | title',len(a["title"]),'| meta',len(a["meta"]),'| banned:',bad or 'OK')
