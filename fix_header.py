# -*- coding: utf-8 -*-
# Header polish across every page (header is baked into each html + read by generators from index.html):
# 1) gap logo<->nav  2) carets point DOWN  3) nav order: אודות first, drop צור קשר
# 4) mobile: תעודת מנעולן מוסמך first, green.
import glob

# --- markup ---
DEL_TAIL='<li><a href="odot.html">אודות</a></li><li><a href="tzor-kesher.html">צור קשר</a></li>'
ANCHOR='<li><a href="sherutim.html">שירותים<span class="caret"'
PREPEND='<li class="m-cert"><a href="tzuda-manulan.html">תעודת מנעולן מוסמך</a></li><li><a href="odot.html">אודות</a></li>'

# --- css targeted ---
CARET_OLD='transform:rotate(-45deg);margin-top:-3px;opacity:.55}'
CARET_NEW='transform:rotate(45deg);margin-top:-2px;opacity:.55}'
HDGAP_OLD='align-items:center;min-height:72px;gap:12px}'
HDGAP_NEW='align-items:center;min-height:72px;gap:24px}'
BRAND_OLD='.brand{display:flex;align-items:center;gap:10px;justify-self:start}'
BRAND_NEW='.brand{display:flex;align-items:center;gap:10px;justify-self:start;margin-inline-end:16px}'
MCERT_CSS=('/* v28-mcert: mobile cert-first (green) */\n'
 '.m-cert{display:none}\n'
 '@media(max-width:980px){.m-cert{display:block}'
 '.m-cert a{background:#1F7A3D;color:#fff!important;font-weight:800;border-radius:10px;'
 'margin:2px 0 8px;justify-content:center;text-align:center}'
 '.m-cert a:hover{color:#fff!important;background:#186a34}}\n')

def fix(s):
    ch=[]
    # 3+4 markup: reorder + drop צור קשר + prepend cert & אודות (guard against double-apply)
    if 'class="m-cert"' not in s and ANCHOR in s:
        s=s.replace(DEL_TAIL,'')                     # remove אודות+צור קשר from tail
        s=s.replace(ANCHOR, PREPEND+ANCHOR, 1)       # prepend cert + אודות before שירותים
        ch.append('nav')
    # 2 carets down
    if CARET_OLD in s: s=s.replace(CARET_OLD,CARET_NEW); ch.append('caret')
    # 1 gap
    if HDGAP_OLD in s: s=s.replace(HDGAP_OLD,HDGAP_NEW); ch.append('gap')
    if BRAND_OLD in s: s=s.replace(BRAND_OLD,BRAND_NEW); ch.append('brand')
    # 4 css
    if 'v28-mcert' not in s and '</style>' in s:
        s=s.replace('</style>', MCERT_CSS+'</style>',1); ch.append('mcertcss')
    return s,ch

tally={}
for fp in glob.glob('/Users/s/niv-locksmith/*.html'):
    s=open(fp,encoding='utf-8').read(); o,ch=fix(s)
    if o!=s: open(fp,'w',encoding='utf-8').write(o)
    for c in ch: tally[c]=tally.get(c,0)+1
print('per-change file counts:',tally)
PY_TOTAL=len(glob.glob('/Users/s/niv-locksmith/*.html'))
print('total html:',PY_TOTAL)
