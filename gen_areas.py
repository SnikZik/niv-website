# -*- coding: utf-8 -*-
import re,json,sys
sys.path.insert(0,'/Users/s/niv-locksmith')
from areas_data import AREAS

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
W='https://wa.me/972508307269?text=%D7%A9%D7%9C%D7%95%D7%9D%20%D7%A0%D7%99%D7%91'
PH='<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.3 1.8.6 2.6a2 2 0 0 1-.5 2.1L8 9.6a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.5c.8.3 1.7.5 2.6.6a2 2 0 0 1 1.7 2Z"/></svg>'
WA='<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-12.3 7.5L3 21l2-5.6A8.4 8.4 0 1 1 21 11.5Z"/></svg>'
CK='<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>'

T={
 "yosi":("הייתה לנו בעיה במנעול העסק. ניב הגיע בזמן, פתר את התקלה במהירות ובמחיר הוגן. ממליץ בחום.","יוסי","ירושלים"),
 "oren":("ננעלתי מחוץ לבית באמצע הלילה. תוך פחות מ-20 דקות ניב היה אצלי, פתח את הדלת בלי נזק והחליף צילינדר חדש. שירות מהיר ואמין.","אורן","ירושלים"),
 "moshe":("קיבלתי יחס אישי ושירות 24/7. הרגשתי שיש על מי לסמוך גם בשעת חירום. תודה על הכל.","משה","ירושלים"),
 "hila":("פניתי לניב בשעת חירום, הדלת לא נסגרה והמשפחה נשארה עם דלת פתוחה. הוא הגיע במהירות, אדיב וסבלני, ופרק והרכיב את הדלת עד שהכל נפתר.","הילה","מודיעין"),
 "meital":("הזמנתי התקנה של מנעול חכם לדלת הבית. קיבלתי ייעוץ מקצועי, הסבר סבלני על כל האפשרויות והתקנה נקייה. מרוצה מאוד.","מיטל","בית שמש"),
}
REVROT=[["oren","moshe"],["yosi","hila"],["meital","oren"],["moshe","yosi"],["hila","meital"]]
ADVROT=[('teal','פותח בזהירות, בלי נזק','ברוב המקרים הדלת נשארת שלמה לגמרי. המטרה שלי שתיכנסו הביתה בלי להחליף כלום.'),
 ('blue','מי שעונה לטלפון הוא מי שמגיע','בלי מוקד, בלי קבלני משנה ובלי הפתעות. סוגרים איתי מחיר בשיחה, ואני זה שדופק בדלת.'),
 ('amber','המחיר נסגר בטלפון, לא בשטח','לפני שאני יוצא אתם יודעים בדיוק כמה זה עולה. מה שסוכם בשיחה הוא מה שמשולם בסוף.'),
 ('indigo','מקומי שמכיר כל שכונה','אני עובד רק בירושלים והסביבה. מכיר את הדלתות של כל שכונה, ולכן מגיע מהר ומוכן.'),
 ('rose','רוב הלקוחות מגיעים בהמלצה','שכן ממליץ לשכן, לקוח מביא לקוח. ככה אני עובד בירושלים כבר שנים, בלי פרסום רועש.')]
SVC_LINKS=[("pritzat-dlatot","פריצת דלתות"),("tzilinder","החלפת צילינדר"),("tikun-dlatot","תיקון דלתות"),
("mamad","דלת ממ״ד"),("manul-hacham","מנעול חכם"),("mafteah-shavur","חילוץ מפתח שבור"),
("ksafot","פריצת כספות"),("manulan-herum","מנעולן חירום 24/7")]

area_css='''
/* areas */
.n6 .bc{background:#fff;border-bottom:1px solid var(--line);font-size:13.5px;padding:8px 0}
.n6 .bc .wrap{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.n6 .bc a{color:var(--iron)} .n6 .bc b{color:var(--ink);font-weight:700}
.n6 .ahero2{background:linear-gradient(180deg,#EAF1F7,#fff);padding:38px 0 34px;border-bottom:1px solid var(--line)}
.n6 .ahero2 h1{font-size:34px;margin-bottom:8px}
.n6 .ahero2 .avail{margin-bottom:14px}
.n6 .ahero2 .sub{font-size:17px;color:var(--ink);max-width:640px;line-height:1.65;margin:12px 0 0}
.n6 .content{max-width:760px;margin-inline:auto;padding:36px 22px}
.n6 .content h2{font-size:24px;margin:28px 0 10px}
.n6 .content h2:first-child{margin-top:0}
.n6 .content p{font-size:16.5px;line-height:1.75;margin-bottom:12px}
.n6 .content a{color:var(--red);font-weight:700;text-decoration:underline;text-underline-offset:3px}
.n6 .svclinks{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:16px 0}
.n6 .svclinks a{display:flex;justify-content:space-between;align-items:center;background:#fff;border:1px solid var(--line);border-radius:11px;padding:14px 16px;font-weight:700;color:var(--ink);text-decoration:none;box-shadow:var(--sh)}
.n6 .svclinks a:hover{color:var(--red)}
.n6 .svclinks a::after{content:"›";color:var(--red);font-weight:800}
.n6 .nearby{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.n6 .nearby a{background:#fff;border:1.5px solid var(--line);border-radius:999px;padding:9px 18px;font-weight:700;font-size:14px;color:var(--ink);text-decoration:none}
.n6 .nearby a:hover{border-color:var(--red);color:var(--red)}
@media(max-width:640px){ .n6 .svclinks{grid-template-columns:1fr} .n6 .ahero2 h1{font-size:28px} }
'''
style2=style.replace('</style>',area_css+'\n</style>')

def page(i,slug,d):
    revs=REVROT[i%5]; advc,advt,advx=ADVROT[i%5][0],ADVROT[i%5][1],ADVROT[i%5][2]
    revh="".join(f'<div class="tcard"><p class="tcard__q">{T[k][0]}</p><div class="tcard__w">{T[k][1]}, <span>{T[k][2]}</span></div></div>' for k in revs)
    svc="".join(f'<a href="{s2}.html">{t} ב{d["b"]}</a>' for s2,t in SVC_LINKS)
    near="".join(f'<a href="{s2}.html">מנעולן ב{n}</a>' for s2,n in d["nearby"])
    faq="".join(f'<div class="faq__i"><button class="faq__q" aria-expanded="false" aria-controls="af{j}">{q}<span class="s" aria-hidden="true">+</span></button><div class="faq__a" id="af{j}">{a}</div></div>' for j,(q,a) in enumerate(d["faq"],1))
    blocks="".join(f'<h2>{h}</h2><p>{t}</p>' for h,t in d["local"])
    mapq=d.get("mapq",d["name"]+" ירושלים")
    import urllib.parse
    mapu="https://www.google.com/maps?q="+urllib.parse.quote(mapq)+"&output=embed&z=14"
    checks="".join(f'<div class="hcheck">{CK}{c}</div>' for c in [f'הגעה ל{d["b"]} בדרך כלל תוך {d["eta"]}','זמין 24/7, גם בלילה ובשבת','מחיר נסגר בטלפון, לפני היציאה'])
    main=f'''
  <nav class="bc" aria-label="פירורי לחם"><div class="wrap"><a href="index.html">בית</a><span aria-hidden="true">›</span><a href="azorei-sherut.html">אזורי שירות</a><span aria-hidden="true">›</span><b>מנעולן ב{d["b"]}</b></div></nav>
  <section class="ahero2"><div class="wrap">
    <h1>מנעולן ב{d["b"]}</h1>
    <p class="avail"><span class="dot" aria-hidden="true"></span>זמין עכשיו · עונה ישירות, בלי מוקד</p>
    <div class="btnrow">
      <a class="btn btn--call btn--lg" href="tel:+972508307269">{PH}חייגו לניב עכשיו</a>
      <a class="btn btn--wa btn--lg" href="{W}" target="_blank" rel="noopener">{WA}שלחו צילום ב-WhatsApp</a>
    </div>
    <div class="pchip" style="margin-top:16px"><b>פריצת דלת מ-300₪</b><span>המחיר נסגר בטלפון, לפני שאני יוצא</span></div>
    <p class="sub">{d["sub"]}</p>
    <div class="hchecks" style="margin-top:16px">{checks}</div>
  </div></section>
  <section class="sec sec--white" style="padding:40px 0 8px"><div class="wrap narrow">
    <div class="defbox" style="background:var(--white);border:1px solid var(--line);border-inline-start:4px solid var(--red);border-radius:12px;padding:22px 24px;box-shadow:var(--sh)">
      <h2 style="font-size:21px;margin-bottom:8px">מנעולן ב{d["b"]}, במשפט אחד</h2>
      <p style="margin:0;font-size:16px">אני ניב, מנעולן מקומי שמגיע ל{d["b"]} בדרך כלל תוך {d["eta"]}. פותח דלתות בזהירות, מחליף צילינדרים ומתקן מנגנונים, זמין 24/7, והמחיר נסגר בטלפון לפני שאני יוצא. חייגו 050-8307269.</p>
    </div>
  </div></section>
  <div class="content">{blocks}</div>
  <section class="emerg">
    <h2>נעולים בחוץ ב{d["b"]}?</h2>
    <p>אני זמין עכשיו. חייגו, תארו מה קרה, ותקבלו מחיר וזמן הגעה כבר בשיחה. ל{d["b"]} אני מגיע בדרך כלל תוך {d["eta"]}.</p>
    <div class="btnrow" style="justify-content:center">
      <a class="btn btn--call btn--lg" href="tel:+972508307269">חייגו 050-8307269</a>
      <a class="btn btn--wa btn--lg" href="{W}" target="_blank" rel="noopener">שלחו WhatsApp</a>
    </div>
  </section>
  <section class="sec sec--white"><div class="wrap narrow">
    <h2 style="font-size:24px">השירותים שלי ב{d["b"]}</h2>
    <p style="color:var(--iron);margin:6px 0 8px">כל שירותי המנעולנות, עד הדלת שלכם. לחצו לשירות לפרטים ומחירים.</p>
    <div class="svclinks">{svc}</div>
  </div></section>
  <section class="adv adv--{advc}"><span class="ic"></span><b>{advt}</b><p>{advx}</p><a href="tel:+972508307269">חייגו לניב 050-8307269</a></section>
  <section class="sec sec--white" style="background:#EFF6F1"><div class="wrap">
    <div class="sh sh--c"><h2>מה לקוחות סיפרו</h2></div>
    <div class="svcrev" style="grid-template-columns:1fr 1fr">{revh}</div>
  </div></section>
  <section class="sec sec--sand"><div class="wrap">
    <div class="sh sh--c"><h2>שאלות על מנעולן ב{d["b"]}</h2></div>
    <div class="faq">{faq}</div>
  </div></section>
  <section class="sec sec--white"><div class="wrap narrow" style="text-align:center">
    <h2 style="font-size:22px;margin-bottom:12px">{d["b"]} על המפה</h2>
    <div style="margin:0 0 18px;border-radius:14px;overflow:hidden;box-shadow:var(--sh)"><iframe loading="lazy" title="מנעולן ב{d["b"]}, אזור שירות" src="{mapu}" style="border:0;width:100%;height:300px;display:block"></iframe></div>
    <h2 style="font-size:19px;margin:18px 0 4px">שכונות סמוכות</h2>
    <div class="nearby" style="justify-content:center">{near}</div>
  </div></section>
  <section class="sec fcta" style="text-align:center;padding:50px 22px">
    <h2 style="font-size:27px;margin-bottom:10px">צריכים מנעולן ב{d["b"]}?</h2>
    <p style="margin-bottom:22px;font-size:17px">חייגו, תארו מה קרה, ותקבלו מחיר וזמן הגעה כבר בשיחה.</p>
    <div class="btnrow" style="justify-content:center">
      <a class="btn btn--call btn--lg" href="tel:+972508307269">חייגו 050-8307269</a>
      <a class="btn btn--wa btn--lg" href="{W}" target="_blank" rel="noopener">שלחו WhatsApp</a>
    </div>
  </section>'''
    ld={"@context":"https://schema.org","@graph":[
     {"@type":"Locksmith","@id":BASE+"/#business","name":"ניב המנעולן","telephone":"+972508307269","url":BASE+"/","priceRange":"₪₪",
      "address":{"@type":"PostalAddress","addressLocality":"ירושלים","addressCountry":"IL"},
      "areaServed":{"@type":"Place","name":d["name"]}},
     {"@type":"Service","name":f'מנעולן ב{d["b"]}',"serviceType":"שירותי מנעולנות","provider":{"@id":BASE+"/#business"},
      "areaServed":{"@type":"Place","name":d["name"]},"url":f'{BASE}/{slug}.html',"description":d["meta"]},
     {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in d["faq"]]},
     {"@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"בית","item":BASE+"/"},
      {"@type":"ListItem","position":2,"name":"אזורי שירות","item":BASE+"/azorei-sherut.html"},
      {"@type":"ListItem","position":3,"name":f'מנעולן ב{d["b"]}',"item":f'{BASE}/{slug}.html'}]}]}
    lds='<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>'
    html=f'''<!doctype html>
<html dir="rtl" lang="he">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{d["title"]}</title>
<meta name="description" content="{d["meta"]}">
<link rel="canonical" href="{BASE}/{slug}.html">
{lds}
{style2}
</head>
<body>
<div class="n6">
{ub}
{header}
{main}
{footer}
{flt}
{smob}
</div>
{js}
</body>
</html>'''
    open(f'/Users/s/niv-locksmith/{slug}.html','w',encoding='utf-8').write(html)
    t=re.sub(r'<script.*?</script>','',html,flags=re.S); t=re.sub(r'<style.*?</style>','',t,flags=re.S); t=re.sub(r'<[^>]+>',' ',t)
    return len(t.split())

banned=["לסיכום","ראשית,","שנית","בנוסף לכך","יתרה מזאת","חשוב לציין","במסגרת","על מנת","כמו כן","יש לציין"]
for i,(slug,d) in enumerate(AREAS.items()):
    w=page(i,slug,d)
    s=open(f'/Users/s/niv-locksmith/{slug}.html',encoding='utf-8').read()
    t=re.sub(r'<script.*?</script>','',s,flags=re.S); t=re.sub(r'<style.*?</style>','',t,flags=re.S); t=re.sub(r'<[^>]+>',' ',t)
    bad=[x for x in banned if x in t]
    print(f'{slug:26} {w:>5}w  {bad or "OK"}')
