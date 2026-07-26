# -*- coding: utf-8 -*-
# Update all prices site-wide to Snir's new מחירון.
# Maps (currency-anchored, base64-safe): 300->350, 499->550, 1,499->2,200.
# Plus targeted rewrites: mehiron rows, manul-hacham table, service note.
import re,glob,os

ROOT='/Users/s/niv-locksmith'

# ---------- targeted edits (structure changes the numeric maps can't do) ----------
TARGETS=[
 # A. mehiron price table source (gen_pages.py): add מנעול מכני 650, split מנעול חכם, כספת 550
 (f'{ROOT}/gen_pages.py',
  'rows=[["פריצת דלת","החל מ-300₪"],["החלפת צילינדר לדלת","החל מ-300₪"],["החלפת צילינדר לדלת פלדלת","החל מ-350₪"],["החלפת ידיות","החל מ-250₪"],["תיקון דלתות","החל מ-350₪"],["התקנת מנעול מכני לדלת","החל מ-550₪"],["התקנת דלת ממ״ד","החל מ-650₪"],["תיקון דלת ממ״ד","החל מ-350₪"],["פריצת כספות","החל מ-350₪"],["התקנת כספת כולל הכספת","החל מ-499₪"],["התקנת מנעול חכם","החל מ-1,499₪"]]',
  'rows=[["פריצת דלת","החל מ-350₪"],["החלפת צילינדר לדלת פנים","החל מ-350₪"],["החלפת צילינדר לדלת פלדלת","החל מ-350₪"],["החלפת ידיות","החל מ-250₪"],["תיקון דלתות","החל מ-350₪"],["התקנת מנעול מכני לדלת","החל מ-650₪"],["התקנת דלת ממ״ד","החל מ-650₪"],["תיקון דלת ממ״ד","החל מ-350₪"],["פריצת כספות","החל מ-350₪"],["התקנת כספת כולל הכספת","החל מ-550₪"],["התקנת מנעול חכם כולל המנעול","החל מ-2,200₪"],["התקנת מנעול חכם","החל מ-500₪"]]'),
 # B. manul-hacham price table (services_deep.py): tiers -> clean 3 rows matching new list
 (f'{ROOT}/services_deep.py',
  "[['מנעול חכם עם קוד', 'מ-1,499₪'], ['מנעול חכם קוד + טביעת אצבע', 'מ-1,799₪'], ['מנעול חכם לפלדלת עם רב בריח', 'מ-2,200₪'], ['צילינדר חכם לדלת קיימת', 'מ-1,200₪']]",
  "[['התקנת מנעול חכם כולל המנעול', 'מ-2,200₪'], ['התקנת מנעול חכם (המנעול שלכם)', 'מ-500₪'], ['צילינדר חכם לדלת קיימת', 'מ-1,200₪']]"),
 # C. service pchip note for manul-hacham (services_data.json): add install-only tier
 (f'{ROOT}/services_data.json',
  '"price_note": "כולל המנעול וההתקנה"',
  '"price_note": "כולל המנעול. התקנה בלבד מ-500₪"'),
]
for fp,old,new in TARGETS:
    s=open(fp,encoding='utf-8').read()
    if old in s:
        s=s.replace(old,new); open(fp,'w',encoding='utf-8').write(s); print('TARGET ok:',os.path.basename(fp))
    elif new in s:
        print('TARGET already:',os.path.basename(fp))
    else:
        print('TARGET MISS:',os.path.basename(fp))

# ---------- global numeric maps (currency-anchored so base64/ids untouched) ----------
CUR=r'(?=\s*(?:₪|שקל|ש["״]ח))'
NB=r'(?<![\d,])'
def fix(s):
    s=re.sub(NB+'300'+CUR,'350',s)
    s=re.sub(NB+'499'+CUR,'550',s)
    s=re.sub(r'1,499'+CUR,'2,200',s)
    s=re.sub(NB+'1499'+CUR,'2200',s)
    # מ--prefixed price forms (comma/period after number, no currency glyph). "מ-" never in base64.
    s=s.replace('מ-1,499','מ-2,200').replace('מ-1499','מ-2200')
    s=s.replace('מ-300','מ-350').replace('מ-499','מ-550')
    return s

SRC=['gen_combo.py','gen_areas.py','gen_article.py','gen_pages.py','gen_services.py',
     'services_deep.py','services_data.json','services_new.py',
     'bank_1.json','bank_2.json','bank_3.json','agent_pz_1.json','agent_pz_2.json','agent_pz_3.json',
     'products_geo.json','products_data.py','areas_data.py']
files=[f'{ROOT}/{x}' for x in SRC if os.path.exists(f'{ROOT}/{x}')]+glob.glob(f'{ROOT}/*.html')
changed=0
for fp in files:
    s=open(fp,encoding='utf-8').read(); o=fix(s)
    if o!=s: open(fp,'w',encoding='utf-8').write(o); changed+=1
print('global price-fix files changed:',changed)
