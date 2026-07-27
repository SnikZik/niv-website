# -*- coding: utf-8 -*-
# Phased publishing: stamp noindex on not-yet-released pages, keep sitemap/llms to live-only.
# Re-run any time (idempotent). Run AFTER any generator so staging survives regeneration.
import json,glob,re,datetime,subprocess,sys
BASE='https://nivlocksmith.co.il'
NOINDEX='<meta name="robots" content="noindex,follow">'

sched=json.load(open('/Users/s/niv-locksmith/publish_schedule.json',encoding='utf-8'))
today=datetime.date.fromisoformat(subprocess.run(['date','+%Y-%m-%d'],capture_output=True,text=True).stdout.strip())

def is_live(b):
    v=sched.get(b,'LIVE')
    if v=='LIVE': return True
    try: return datetime.date.fromisoformat(v)<=today
    except: return True

live=[]; staged=[]
for f in glob.glob('/Users/s/niv-locksmith/*.html'):
    b=f.split('/')[-1][:-5]
    s=open(f,encoding='utf-8').read()
    has=NOINDEX in s
    if is_live(b):
        if has: s=s.replace('\n'+NOINDEX,'').replace(NOINDEX,''); open(f,'w',encoding='utf-8').write(s)
        live.append(b)
    else:
        if not has:
            s=s.replace('<meta name="viewport" content="width=device-width, initial-scale=1">',
                        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'+NOINDEX,1)
            open(f,'w',encoding='utf-8').write(s)
        staged.append(b)

# rebuild sitemap: live only
def pr(b):
    if b=='index': return '1.0'
    if b in ('mehiron','azorei-sherut','madrichim','tzor-kesher','odot'): return '0.8'
    if b.startswith('mutzar-'): return '0.6'
    if b.startswith('katalog'): return '0.7'
    return '0.8'
urls=sorted(live)
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemap.org/schemas/sitemap/0.9">\n'.replace('sitemap.org','sitemaps.org')
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for b in urls:
    loc=f'{BASE}/' if b=='index' else f'{BASE}/{b}.html'
    sm+=f'<url><loc>{loc}</loc><priority>{pr(b)}</priority></url>\n'
sm+='</urlset>\n'
open('/Users/s/niv-locksmith/sitemap.xml','w',encoding='utf-8').write(sm)

print(f'live: {len(live)} | staged(noindex): {len(staged)} | sitemap urls: {len(urls)}')
# next release preview
future={}
for b,v in sched.items():
    if v=='LIVE': continue
    try:
        d=datetime.date.fromisoformat(v)
        if d>today: future.setdefault(v,0); future[v]+=1
    except: pass
nxt=sorted(future)[:3]
for d in nxt: print(f'  upcoming {d}: {future[d]} pages')
