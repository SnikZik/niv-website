# -*- coding: utf-8 -*-
import re,json,sys
sys.path.insert(0,'/Users/s/niv-locksmith')
from catalog_data import CATS
from catalog_data2 import CATS2
ALL={**CATS,**CATS2}
RICH=json.load(open('/Users/s/niv-locksmith/products_rich.json',encoding='utf-8'))
BASE='https://snikzik.github.io/niv-website'
W='https://wa.me/972508307269?text=%D7%A9%D7%9C%D7%95%D7%9D%20%D7%A0%D7%99%D7%91'

# shared shell pieces from a light source (use catalog page, strip style -> external css)
src=open('/Users/s/niv-locksmith/katalog-manulim.html',encoding='utf-8').read()
ub=re.search(r'<div class="ub">.*?</div></div>',src,re.S).group(0)
header=re.search(r'<header class="hd">.*?</header>',src,re.S).group(0)
footer=re.search(r'<footer class="ft">.*?</footer>',src,re.S).group(0)
flt=re.search(r'<div class="float">.*?</div>\s*(?=<div class="smob">)',src,re.S).group(0)
smob=re.search(r'<div class="smob">.*?</div>\s*(?=</div>)',src,re.S).group(0)
js=re.search(r'<script>.*?</script>',src,re.S).group(0)

TR={'א':'a','ב':'b','ג':'g','ד':'d','ה':'h','ו':'o','ז':'z','ח':'ch','ט':'t','י':'i','כ':'k','ך':'k','ל':'l','מ':'m','ם':'m','נ':'n','ן':'n','ס':'s','ע':'a','פ':'p','ף':'f','צ':'tz','ץ':'tz','ק':'k','ר':'r','ש':'sh','ת':'t','״':'','"':'','׳':'',"'":''}
def slugify(name):
    s=name.lower()
    out=[]
    for ch in s:
        if ch in TR: out.append(TR[ch])
        elif ch.isascii() and (ch.isalnum()): out.append(ch)
        elif ch in ' -/+.,':
            out.append('-')
    sl=re.sub(r'-+','-',''.join(out)).strip('-')
    return sl[:60] or 'prod'

# image pools by tag keyword
import os,hashlib
POOL={}
for f in os.listdir('/Users/s/niv-locksmith/img/products'):
    if not f.endswith('.jpg'): continue
    base=f[:-4]
    root=base.rsplit('-',1)[0] if base.rsplit('-',1)[-1].isdigit() else base
    POOL.setdefault(root,[]).append(base)
def pick(tag,name):
    opts=sorted(POOL.get(tag,[tag]))
    h=int(hashlib.md5(name.encode()).hexdigest(),16)
    return opts[h%len(opts)]
def img_for(cat_slug, tag, name):
    n=name.lower()
    def has(*ws): return any(w in n for w in ws)
    if has('אופניים'): return 'bike'
    if has('tsa','נסיעות'): return 'travel'
    if has('פליז'): return 'padlock-brass'
    if has('תלי','תליה','pdlock','פבלוק','רתק'): return 'padlock'
    if has('צילינדר'): return 'cylinder' if 'smartair' not in n else 'smartair'
    if has('כספת') and has('אש'): return 'safe-fire'
    if has('כספת'): return 'safe'
    if has('רצפתי') or has('זכוכית') and 'מחזיר' in n: return 'closer-floor'
    if has('מחזיר','מתאם סגירה','סגר'): return 'closer'
    if has('בהלה'): return 'panic'
    if has('מגנט','אלקטרו מגנטי','אלקטרומגנט','securitron','gl-'): return 'magnet'
    if has('בריח חשמלי','נגדי','effeff','חשמלי'): return 'electric'
    if has('קודן') and not has('מנעול חכם'): return 'keypad'
    if has('עינית'): return 'peephole'
    if has('פעמון'): return 'doorbell'
    if has('מצלמ'): return 'camera'
    if has('linus','חכם','smart2','dot','entr','סוללה','מגשר'): return 'smart'
    if has('smartair','aperio','incedo','sparkey','קורא','בקר','כרטיס','תג','מפתחות בנייד','לוקר','ארונית','ks200'): return 'access'
    if has('ידית','פרזול','פלטת'): return 'handle'
    if has('ציר'): return 'hinge'
    if has('מלון','חסכן','spy'): return 'hotel'
    if has('חיישן','flatscan','magic','eagle','פותח'): return 'sensor'
    return 'generic'

def img_for_final(cat_slug,tag,name):
    return pick(img_for(cat_slug,tag,name),name)

# category-level content pools (3 sections × variants)
POOLS={
 "default":{
  "why":["הדגם הזה נמצא בקטלוג שלי כי הוא מהסוג שמחזיק שנים בשטח הירושלמי. אני בוחר לקטלוג רק מוצרים שראיתי עובדים לאורך זמן אצל לקוחות, בלי תקלות חוזרות ובלי חלקים שנעלמים מהשוק.",
   "בחרתי להכניס את הדגם הזה לקטלוג אחרי שהוכיח את עצמו בהתקנות אמיתיות. אני לא מחזיק מוצרים שמייצרים לי קריאות שירות, ולכן מה שמופיע כאן הוא בדיוק מה שהייתי מתקין בבית של עצמי.",
   "המוצר הזה עומד בשלושת המבחנים שלי לקטלוג, אמינות מוכחת לאורך שנים, חלפים וגיבוי יצרן זמינים בארץ, ויחס הוגן בין מחיר לתמורה. פחות ברק שיווקי, יותר עבודה שקטה."],
  "fit":["ההתאמה לדלת ולצורך שלכם נעשית בשיחה קצרה, מה הדלת, מה השימוש, ומה חשוב לכם. אם הדגם הזה לא מתאים בדיוק, אגיד ביושר ואציע את הנכון, גם אם הוא זול יותר.",
   "לפני שסוגרים על הדגם, אני בודק התאמה, מידות הדלת, סוג המנגנון הקיים ותנאי הסביבה. צילום אחד בוואטסאפ נותן לי את רוב התשובות, והשאר נסגר בשיחה של דקות.",
   "כמו כל מוצר בקטלוג, גם כאן ההתאמה קודמת למכירה. תיאור קצר של הדלת והצורך, ואגיד לכם אם זה הדגם הנכון או שיש התאמה טובה יותר בקטגוריה."],
  "install":["ההתקנה נעשית על ידי אישית, עם כיול ובדיקה מלאה בסיום, ואחריות על העבודה. המחיר שנסגר בטלפון כולל את המוצר ואת ההתקנה, בלי הפתעות.",
   "אני מתקין את המוצר בעצמי, מכוון אותו לדלת שלכם ומדגים שהכל עובד לפני שאני עוזב. אחריות יצרן על המוצר ואחריות שלי על ההתקנה, הכל בקבלה מסודרת.",
   "התקנה מקצועית היא חצי מהמוצר, ולכן אני לא מוכר בלעדיה. אתם מקבלים התקנה מדויקת, הדרכה קצרה על השימוש, וכתובת אחת לכל שאלה בהמשך."]},
}
FAQ_POOL={
 "default":[
  ("אפשר לקנות את המוצר בלי התקנה?","הקטלוג שלי עובד במודל של מוצר עם התקנה, כי התקנה נכונה היא מה שהופך מוצר טוב לפתרון אמין. המחיר הכולל נסגר בטלפון."),
  ("כמה עולה הדגם הזה?","המחיר תלוי בתצורה ובדלת שלכם, ולכן אני נותן אותו בטלפון אחרי התאמה קצרה. מה שנסגר בשיחה הוא המחיר הסופי, כולל התקנה."),
  ("יש אחריות?","כן, אחריות יצרן על המוצר ואחריות שלי על ההתקנה. תקלה בתקופת האחריות מטופלת בלי חשבון נוסף."),
  ("תוך כמה זמן מתקינים?","ברוב המקרים תוך יום עד שלושה מרגע הסגירה, ולעבודות דחופות גם באותו יום. ההתקנה עצמה נמשכת בדרך כלל פחות משעתיים."),
  ("מה אם הדגם לא מתאים לדלת שלי?","בדיוק בשביל זה יש את שיחת ההתאמה לפני. אם משהו לא מתאים, אציע חלופה נכונה מהקטלוג, ולא אתקין מוצר שלא ישרת אתכם."),
 ]}

def page(cat_slug,cat,prod,idx,all_prods):
    name=prod['name']; tag=prod.get('tag',''); desc=prod['desc']
    pslug='mutzar-'+slugify(name)
    img=img_for_final(cat_slug,tag,name)
    p=POOLS['default']; fq=FAQ_POOL['default']
    R=RICH.get(name)
    if R:
        why=R['long']; fit=R['fit']; inst=R['install']; sku=R['sku']
        specs_html='<ul style="margin:14px 0 0;padding-inline-start:20px">'+''.join(f'<li style="font-size:15px;line-height:1.65;margin-bottom:5px">{x}</li>' for x in R['specs'])+'</ul>'
    else:
        why=p['why'][idx%3]; fit=p['fit'][(idx+1)%3]; inst=p['install'][(idx+2)%3]; sku=''; specs_html=''
    faqs=[fq[idx%5],fq[(idx+2)%5],fq[(idx+4)%5]]
    faqh="".join(f'<div class="faq__i"><button class="faq__q" aria-expanded="false" aria-controls="pf{j}">{q}<span class="s" aria-hidden="true">+</span></button><div class="faq__a" id="pf{j}">{a}</div></div>' for j,(q,a) in enumerate(faqs,1))
    rel=[x for x in all_prods if x['name']!=name][:4]
    relh="".join(f'<a class="pcard" href="mutzar-{slugify(x["name"])}.html"><span class="pcard__img"><img src="img/products/{img_for_final(cat_slug,x.get("tag",""),x["name"])}.jpg" alt="{x["name"]}" loading="lazy"></span><span class="tag">{x.get("tag","")}</span><b>{x["name"]}</b><p>{x["desc"]}</p><span class="ask">לעמוד המוצר ›</span></a>' for x in rel)
    title=f'{name} | {cat["h1"]} | ניב המנעולן'[:65]
    meta=(f'{name}, {desc} ייעוץ, אספקה והתקנה בירושלים על ידי ניב המנעולן. המחיר נסגר בטלפון. חייגו 050-8307269.')[:160]
    ld={"@context":"https://schema.org","@graph":[
     {"@type":"Product","name":name,"description":desc,"sku":RICH.get(name,{}).get("sku",""),"image":f'{BASE}/img/products/{img}.jpg',
      "brand":{"@type":"Brand","name":tag if tag and tag[0].isascii() else "ניב המנעולן"},

      "seller":{"@type":"Locksmith","name":"ניב המנעולן","telephone":"+972508307269"}},
     {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]},
     {"@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"בית","item":BASE+"/"},
      {"@type":"ListItem","position":2,"name":"קטלוג מוצרים","item":BASE+"/katalog.html"},
      {"@type":"ListItem","position":3,"name":cat["h1"],"item":f'{BASE}/{cat_slug}.html'},
      {"@type":"ListItem","position":4,"name":name,"item":f'{BASE}/{pslug}.html'}]}]}
    lds='<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False)+'</script>'
    html=f'''<!doctype html>
<html dir="rtl" lang="he">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="{BASE}/{pslug}.html">
<link rel="stylesheet" href="assets/style.css">
{lds}
</head>
<body>
<div class="n6">
{ub}
{header}
  <nav class="bc" aria-label="פירורי לחם"><div class="wrap"><a href="index.html">בית</a><span aria-hidden="true">›</span><a href="katalog.html">קטלוג</a><span aria-hidden="true">›</span><a href="{cat_slug}.html">{cat["h1"]}</a><span aria-hidden="true">›</span><b>{name}</b></div></nav>
  <section class="phero" style="padding-bottom:24px"><div class="wrap">
    <span style="display:inline-block;background:#fff;border:1px solid var(--line);border-radius:999px;color:var(--red);font-weight:800;font-size:13px;padding:5px 14px;margin-bottom:12px">{tag}</span>
    <h1 style="font-size:30px">{name}</h1>
    {'<p style="color:var(--iron);font-size:13.5px;margin-top:6px">מק״ט: <b style="color:var(--ink)">'+sku+'</b></p>' if sku else ''}
    <p style="font-size:17px;color:var(--iron);max-width:640px;line-height:1.65">{desc}</p>
  </div></section>
  <section class="sec sec--white" style="padding:34px 0 10px"><div class="wrap narrow">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:26px;align-items:start" class="prodgrid">
      <div style="border-radius:14px;overflow:hidden;box-shadow:var(--sh)"><img src="img/products/{img}.jpg" alt="{name}, אספקה והתקנה בירושלים" style="width:100%;display:block" loading="eager"></div>
      <div>
        <h2 style="font-size:21px;margin-bottom:8px">למה הדגם הזה בקטלוג שלי</h2>
        <p style="font-size:15.5px;line-height:1.7;margin-bottom:14px">{why}</p>
        <div class="btnrow">
          <a class="btn btn--call" href="tel:+972508307269">התייעצות על הדגם, 050-8307269</a>
          <a class="btn btn--wa" href="{W}" target="_blank" rel="noopener">שלחו צילום דלת ב-WhatsApp</a>
        </div>
      </div>
    </div>
  </div></section>
  <div class="content" style="padding-top:20px">
    {'<h2>מפרט עיקרי</h2>'+specs_html if specs_html else ''}
    <h2>התאמה לדלת ולצורך שלכם</h2><p>{fit}</p>
    <h2>אספקה והתקנה בירושלים</h2><p>{inst}</p>
  </div>
  <section class="sec sec--sand"><div class="wrap"><div class="sh sh--c"><h2>שאלות על {name}</h2></div><div class="faq">{faqh}</div></div></section>
  <section class="sec sec--white"><div class="wrap">
    <div class="sh sh--c"><h2>עוד מ{cat["h1"]}</h2></div>
    <div class="pgrid" style="grid-template-columns:repeat(4,1fr)">{relh}</div>
    <p style="text-align:center;margin-top:18px"><a href="{cat_slug}.html" style="color:var(--red);font-weight:800">לכל {cat["h1"]} ›</a></p>
  </div></section>
  <section class="sec fcta" style="text-align:center;padding:46px 22px">
    <h2 style="font-size:25px;margin-bottom:10px">רוצים את {name}?</h2>
    <p style="margin-bottom:20px;font-size:16.5px">שיחת התאמה קצרה, מחיר כולל התקנה, ותיאום ליום שנוח לכם.</p>
    <div class="btnrow" style="justify-content:center">
      <a class="btn btn--call btn--lg" href="tel:+972508307269">חייגו 050-8307269</a>
      <a class="btn btn--wa btn--lg" href="{W}" target="_blank" rel="noopener">שלחו WhatsApp</a>
    </div>
  </section>
{footer}
{flt}
{smob}
</div>
{js}
</body>
</html>'''
    open(f'/Users/s/niv-locksmith/{pslug}.html','w',encoding='utf-8').write(html)
    return pslug,img

made={}
for cat_slug,cat in ALL.items():
    for i,prod in enumerate(cat['products']):
        pslug,img=page(cat_slug,cat,prod,i,cat['products'])
        made[prod['name']]=(pslug,img,cat_slug)
print("product pages:",len(made))
json.dump({k:{'slug':v[0],'img':v[1],'cat':v[2]} for k,v in made.items()},open('/Users/s/niv-locksmith/products_index.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
