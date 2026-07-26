# -*- coding: utf-8 -*-
# One-command tracking activation. Fill the 3 IDs, run once. Injects GA4 + (optional) GTM
# + Google Search Console verification into EVERY html page and into all generators.
# Re-runnable / idempotent. Usage: python3 inject_tracking.py
import glob,re

# ===== FILL THESE (leave '' to skip) =====
GA4_ID   = ''            # e.g. 'G-XXXXXXXXXX'  (Google Analytics 4)
GTM_ID   = ''            # e.g. 'GTM-XXXXXXX'   (optional Tag Manager; if set, prefer over raw GA4)
GSC_META = ''            # e.g. 'abcd1234...'   (Search Console meta verification content)
# =========================================

MARK='<!--TRACKING-->'

def head_block():
    b=MARK+'\n'
    if GSC_META:
        b+=f'<meta name="google-site-verification" content="{GSC_META}">\n'
    if GTM_ID:
        b+=("<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});"
            "var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;"
            "j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})"
            f"(window,document,'script','dataLayer','{GTM_ID}');</script>\n")
    if GA4_ID and not GTM_ID:
        b+=(f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>\n'
            "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
            f"gtag('js',new Date());gtag('config','{GA4_ID}');</script>\n")
    b+=MARK
    return b

def body_gtm():
    if not GTM_ID: return ''
    return (f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" '
            'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>')

def strip_old(s):
    return re.sub(re.escape(MARK)+r'.*?'+re.escape(MARK), '', s, flags=re.S)

blk=head_block()
n=0
for fp in glob.glob('/Users/s/niv-locksmith/*.html'):
    s=open(fp,encoding='utf-8').read(); o=s
    s=strip_old(s)
    if (GA4_ID or GTM_ID or GSC_META) and '</head>' in s:
        s=s.replace('</head>', blk+'\n</head>', 1)
        bg=body_gtm()
        if bg and '<body>' in s: s=s.replace('<body>','<body>\n'+bg,1)
    if s!=o: open(fp,'w',encoding='utf-8').write(s); n+=1
print('pages updated:',n)

# also patch generators so regen keeps tracking (insert block before </head> in their templates)
if GA4_ID or GTM_ID or GSC_META:
    for g in glob.glob('/Users/s/niv-locksmith/gen_*.py'):
        s=open(g,encoding='utf-8').read()
        if MARK in s: continue
        # generators emit head via link rel="canonical"... insert block string after it once
        if 'rel="canonical"' in s and 'TRACKING' not in s:
            print('NOTE: add tracking to generator manually if needed:',g.split("/")[-1])
print('done. Re-run after changing IDs.')
