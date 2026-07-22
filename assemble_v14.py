import re,os
OLD=os.environ["OLD"]
PREV="/Users/s/niv-locksmith/preview/v13test.html"
v13=open(PREV,encoding="utf-8").read()
base_css=re.search(r"<style>(.*?)</style>", v13, re.S).group(1)
add=open(os.path.join(OLD,"niv-v14-additions.css"),encoding="utf-8").read()
css=base_css+"\n"+add
body=open(os.path.join(OLD,"niv-v14-body.html"),encoding="utf-8").read()
imgs={}
for m in re.finditer(r'<img\s+src="(data:[^"]+)"\s+alt="([^"]*)"', v13):
    src,alt=m.group(1),m.group(2)
    if "מחזיק צילינדר" in alt: imgs["HERO1"]=src
    elif "מנגנון" in alt: imgs["HERO2"]=src
    elif alt=="ניב המנעולן": imgs["EMBLEM"]=src
for k in ("EMBLEM","HERO1","HERO2"):
    if k in imgs: body=body.replace("__%s__"%k, imgs[k])
missing=[t for t in ("__EMBLEM__","__HERO1__","__HERO2__") if t in body]
js="""
<script>
document.querySelectorAll('.faq__q').forEach(function(b){b.addEventListener('click',function(){var open=b.getAttribute('aria-expanded')==='true';b.setAttribute('aria-expanded',(!open).toString());var a=b.nextElementSibling;if(a){a.style.maxHeight=open?null:(a.scrollHeight+'px');}var s=b.querySelector('.s');if(s)s.textContent=open?'+':'\\u2212';});});
var bg=document.querySelector('.burger'),nv=document.getElementById('niv-mainnav');
if(bg&&nv){bg.addEventListener('click',function(){var o=bg.getAttribute('aria-expanded')==='true';bg.setAttribute('aria-expanded',(!o).toString());nv.classList.toggle('open',!o);document.body.classList.toggle('navopen',!o);});}
</script>
"""
title="מנעולן לדלתות בירושלים | ניב המנעולן 050-8307269"
desc="מנעולן לדלתות בירושלים והסביבה, זמין 24/7. פריצת דלתות, החלפת צילינדר, תיקון דלתות, כספות ומנעולים חכמים. מדברים ישירות עם ניב. חייגו 050-8307269."
html='<!doctype html>\n<html dir="rtl" lang="he">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>'+title+'</title>\n<meta name="description" content="'+desc+'">\n<style>\n'+css+'\n</style>\n</head>\n<body>\n'+body+js+'\n</body>\n</html>'
open("/Users/s/niv-locksmith/preview/v14test.html","w",encoding="utf-8").write(html)
open("/Users/s/niv-locksmith/index.html","w",encoding="utf-8").write(html)
text=re.sub(r"<[^>]+>"," ",body); text=re.sub(r"\s+"," ",text).strip(); words=text.split(" ")
banned=["לסיכום","ראשית","שנית","בנוסף לכך","יתרה מזאת","חשוב לציין","במסגרת","על מנת","כמו כן","יש לציין","בעידן המודרני","פתרון מקיף","ללא פשרות"]
print("wrote v14test.html + index.html",len(html),"bytes | imgs:",list(imgs.keys()),"| missing:",missing)
print("BODY WORDS:",len(words),"| H1:",html.count("<h1"),"H2:",html.count("<h2"),"scards:",body.count('class="scard"'),"prows:",body.count('class="prow"'),"tcards:",body.count('class="tcard"'))
print("banned AI words:",[w for w in banned if w in text] or "NONE")
print("keyword first100:","מנעולן לדלתות בירושלים" in " ".join(words[:100]))
