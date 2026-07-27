# -*- coding: utf-8 -*-
# Post-process (run AFTER generators, like apply_staging):
#  1) inject the comprehensive business @graph (BIZ+PERSON) into any page missing it
#  2) inject Open Graph + Twitter card meta into every page (built from its own title/desc/canonical)
# Idempotent + re-runnable.
import re, json, glob
from schema_business import BIZ, PERSON, BASE

BIZLD = ('<!--BIZLD--><script type="application/ld+json">'
         + json.dumps({"@context": "https://schema.org", "@graph": [BIZ, PERSON]}, ensure_ascii=False)
         + '</script><!--/BIZLD-->')
OG_IMG = BASE + '/img/niv/about-banner.jpg'
SITE = 'ניב המנעולן'

def has_full_biz(s):
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: d = json.loads(b)
        except: continue
        for n in (d.get('@graph', [d]) if isinstance(d, dict) else []):
            if n.get('@type') == 'Locksmith' and len(n.get('areaServed', [])) >= 30:
                return True
    return False

def og_block(s):
    t = re.search(r'<title>(.*?)</title>', s, re.S)
    d = re.search(r'<meta name="description" content="(.*?)"', s, re.S)
    c = re.search(r'<link rel="canonical" href="(.*?)"', s)
    title = (t.group(1) if t else SITE).strip()
    desc = (d.group(1) if d else '').strip()
    url = c.group(1) if c else BASE + '/'
    def esc(x): return x.replace('"', '&quot;')
    return ('<!--OGTAGS-->'
            f'<meta property="og:type" content="website">'
            f'<meta property="og:site_name" content="{SITE}">'
            f'<meta property="og:locale" content="he_IL">'
            f'<meta property="og:title" content="{esc(title)}">'
            f'<meta property="og:description" content="{esc(desc)}">'
            f'<meta property="og:url" content="{url}">'
            f'<meta property="og:image" content="{OG_IMG}">'
            f'<meta name="twitter:card" content="summary_large_image">'
            f'<meta name="twitter:title" content="{esc(title)}">'
            f'<meta name="twitter:description" content="{esc(desc)}">'
            f'<meta name="twitter:image" content="{OG_IMG}">'
            '<!--/OGTAGS-->')

biz_n = og_n = 0
for f in glob.glob('/Users/s/niv-locksmith/*.html'):
    s = open(f, encoding='utf-8').read(); o = s
    if '</head>' not in s:
        continue
    # 1) business schema where missing
    if '<!--BIZLD-->' not in s and not has_full_biz(s):
        s = s.replace('</head>', BIZLD + '\n</head>', 1); biz_n += 1
    # 2) OG/Twitter where missing
    if '<!--OGTAGS-->' not in s and 'og:title' not in s:
        s = s.replace('</head>', og_block(s) + '\n</head>', 1); og_n += 1
    if s != o:
        open(f, 'w', encoding='utf-8').write(s)
print('BIZ injected into:', biz_n, '| OG/Twitter injected into:', og_n)
