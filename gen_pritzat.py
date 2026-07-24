# -*- coding: utf-8 -*-
# premium pritzat-dlatot × area pages from agent JSON
import re,json,sys,os,urllib.parse
sys.path.insert(0,'/Users/s/niv-locksmith')
from areas_data import AREAS
from gen_combo import (style,ub,header,footer,flt,smob,js,BASE,WAURL,PIDX,STRIP,
                       T,REVROT,ADV,CAM,SVCS,pick,pidx)

ARTS=[]
for i in (1,2,3):
    fp=f'/Users/s/niv-locksmith/agent_pz_{i}.json'
    if os.path.exists(fp): ARTS+=json.load(open(fp,encoding='utf-8'))

banned=["לסיכום","ראשית,","שנית,","בנוסף לכך","יתרה מזאת","חשוב לציין","במסגרת","על מנת","כמו כן","יש לציין","—","–"]
n=0
for ai,a in enumerate(ARTS):
    slug=a['slug']; A=a['area']; E=a['eta']; area_slug=a['area_slug']
    d=AREAS[area_slug] if isinstance(AREAS,dict) else next(x for x in AREAS if x['slug']==area_slug)
    short=area_slug.replace('manulan-','')
    blk=a['blocks']
    body_top="".join(blk[:2])
    body_rest="".join(blk[2:])
    faqs=a['faq']
    faq_html="".join(f'<div class="faq__i"><button class="faq__q" aria-expanded="false" aria-controls="cf{j}">{q}<span class="s" aria-hidden="true">+</span></button><div class="faq__a" id="cf{j}">{ans}</div></div>' for j,(q,ans) in enumerate(faqs,1))
    svc_links="".join(f'<a href="{s2}-{short}.html">{t2} ב{A}</a>' for s2,t2 in SVCS if s2!='pritzat-dlatot')
    near="".join(f'<a href="{s2}.html">מנעולן ב{n2}</a>' for s2,n2 in d['nearby'])
    revs=REVROT[ai%5]
    revh="".join(f'<div class="tcard"><p class="tcard__q">{T[k][0]}</p><div class="tcard__w">{T[k][1]}, <span>{T[k][2]}</span></div></div>' for k in revs)
    mapq=d.get('mapq',d['name']+' ירושלים')
    mapu='https://www.google.com/maps?q='+urllib.parse.quote(mapq)+'&output=embed&z=14'
    strip_cards=''
    for nname in STRIP['pritzat-dlatot']:
        p=PIDX.get(nname)
        if p: strip_cards+=f'<a class="pcard" href="{p["slug"]}.html"><span class="pcard__img"><img src="img/products/{p["img"]}.jpg" alt="{nname}" loading="lazy"></span><b>{nname}</b><span class="ask">לעמוד המוצר ›</span></a>'
    g,bt,bx,bhref,bcta=ADV[ai%5]
    tb=' target="_blank" rel="noopener"' if 'wa.me' in bhref else ''
    adv=f'<section class="adv" style="background:{g}">{CAM}<b>{bt}</b><p>{bx}</p><a href="{bhref}"{tb}>{bcta}</a></section>'
    faq_ld=[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',ans)}} for q,ans in faqs]
    graph=[{"@type":"Locksmith","@id":BASE+"/#business","name":"ניב המנעולן","telephone":"+972508307269","url":BASE+"/",
      "address":{"@type":"PostalAddress","addressLocality":"ירושלים","addressCountry":"IL"}},
     {"@type":"Service","name":a['h1'],"serviceType":"פריצת דלתות",
      "provider":{"@id":BASE+"/#business"},"areaServed":{"@type":"Place","name":f'{A}, ירושלים'},
      "url":f'{BASE}/{slug}.html'},
     {"@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"בית","item":BASE+"/"},
      {"@type":"ListItem","position":2,"name":"אזורי שירות","item":BASE+"/azorei-sherut.html"},
      {"@type":"ListItem","position":3,"name":f'מנעולן ב{A}',"item":f'{BASE}/{area_slug}.html'},
      {"@type":"ListItem","position":4,"name":a['h1'],"item":f'{BASE}/{slug}.html'}]},
     {"@type":"FAQPage","mainEntity":faq_ld}]
    ld='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@graph":graph},ensure_ascii=False)+'</script>'
    main=f'''
  <nav class="bc" aria-label="פירורי לחם"><div class="wrap"><a href="index.html">בית</a><span aria-hidden="true">›</span><a href="azorei-sherut.html">אזורי שירות</a><span aria-hidden="true">›</span><a href="{area_slug}.html">מנעולן ב{A}</a><span aria-hidden="true">›</span><b>{a['h1']}</b></div></nav>
  <section class="ahero2"><div class="wrap">
    <span class="k">פריצת דלתות · {A} · הגעה {E}</span>
    <h1>{a['h1']}</h1>
    <p class="lead">{a['lead']}</p>
    <div class="btnrow"><a class="btn btn--call btn--lg" href="tel:+972508307269">חייגו 050-8307269</a>
    <a class="btn btn--wa btn--lg" href="{WAURL}" target="_blank" rel="noopener">שלחו WhatsApp</a></div>
  </div></section>
  <section class="sec sec--white"><div class="wrap narrow content">
    {body_top}
  </div></section>
  <section class="sec sec--white" style="background:#F6F3FB"><div class="wrap"><div class="sh sh--c"><h2>מהקטלוג שלי</h2><p>עם ייעוץ והתקנה. המחיר נסגר בטלפון.</p></div><div class="pgrid" style="grid-template-columns:repeat(4,1fr)">{strip_cards}</div></div></section>
  <section class="sec sec--white"><div class="wrap narrow content">
    {body_rest}
  </div></section>
  {adv}
  <section class="sec sec--sand"><div class="wrap">
    <div class="sh sh--c"><h2>מה לקוחות מספרים</h2></div>
    <div class="tgrid" style="grid-template-columns:repeat(2,1fr);max-width:760px;margin-inline:auto">{revh}</div>
  </div></section>
  <section class="sec sec--sand"><div class="wrap">
    <div class="sh sh--c"><h2>שאלות על {a['h1']}</h2></div>
    <div class="faq">{faq_html}</div>
  </div></section>
  <section class="sec sec--white"><div class="wrap">
    <h2 style="font-size:24px">עוד שירותים ב{A}</h2>
    <div class="svclinks">{svc_links}</div>
    <h2 style="font-size:24px;margin-top:26px">אזור השירות</h2>
    <div style="margin:12px 0 18px;border-radius:14px;overflow:hidden;box-shadow:var(--sh)"><iframe loading="lazy" title="{a['h1']}, אזור שירות" src="{mapu}" style="border:0;width:100%;height:300px;display:block"></iframe></div>
    <div class="nearby">{near}</div>
  </div></section>
  <section class="sec fcta" style="text-align:center;padding:50px 22px">
    <h2 style="font-size:27px;margin-bottom:10px">צריכים פריצת דלת ב{A}?</h2>
    <p style="margin-bottom:22px;font-size:17px">חייגו, תארו מה קרה, ותקבלו מחיר וזמן הגעה כבר בשיחה.</p>
    <div class="btnrow" style="justify-content:center">
      <a class="btn btn--call btn--lg" href="tel:+972508307269">חייגו 050-8307269</a>
      <a class="btn btn--wa btn--lg" href="{WAURL}" target="_blank" rel="noopener">שלחו WhatsApp</a>
    </div>
  </section>'''
    html=f'<!doctype html>\n<html dir="rtl" lang="he">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>{a["title"]}</title>\n<meta name="description" content="{a["meta"]}">\n<link rel="canonical" href="{BASE}/{slug}.html"><link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png"><link rel="icon" type="image/png" sizes="16x16" href="favicon-16.png"><link rel="icon" href="favicon.ico"><link rel="apple-touch-icon" href="apple-touch-icon.png">\n{ld}\n{style}\n</head>\n<body>\n<div class="n6">\n{ub}\n{header}\n{main}\n{footer}\n{flt}\n{smob}\n</div>\n{js}\n</body>\n</html>'
    bad=[w for w in banned if w in html]
    t=re.sub(r'<script.*?</script>','',html,flags=re.S); t=re.sub(r'<style.*?</style>','',t,flags=re.S); t=re.sub(r'<[^>]+>',' ',t)
    open(f'/Users/s/niv-locksmith/{slug}.html','w',encoding='utf-8').write(html)
    print(slug,len(t.split()),'w | title',len(a['title']),'| meta',len(a['meta']),'| bad:',bad or 'OK')
    n+=1
print('premium pages:',n)
