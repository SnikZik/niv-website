# -*- coding: utf-8 -*-
"""Merge agent JSONs into areas_data.py, validate, regen, wire hub+llms+sitemap."""
import json,re,sys,glob
sys.path.insert(0,'/Users/s/niv-locksmith')

BANNED=["לסיכום","ראשית,","שנית","בנוסף לכך","יתרה מזאת","חשוב לציין","במסגרת","על מנת","כמו כן","יש לציין","ללא פשרות","—"]
VALID={"manulan-pisgat-zeev","manulan-neve-yaakov","manulan-ramot","manulan-ramat-shlomo","manulan-french-hill","manulan-ramat-eshkol","manulan-romema","manulan-givat-shaul","manulan-beit-hakerem","manulan-kiryat-yovel","manulan-kiryat-menachem","manulan-gilo","manulan-har-homa","manulan-talpiot","manulan-arnona","manulan-baka","manulan-katamon","manulan-rehavia","manulan-nachlaot","manulan-merkaz-hair","manulan-geula","manulan-har-nof","manulan-givat-mordechai","manulan-malha","manulan-ramat-sharet","manulan-old-city","manulan-givat-zeev","manulan-mevaseret","manulan-maale-adumim","manulan-abu-gosh","manulan-motza"}

def clean(o):
    if isinstance(o,str):
        s=o.replace('—',', ').replace('לסיכום,','').replace('על מנת','כדי').replace('כמו כן,','וגם').replace('במסגרת','בתוך')
        return re.sub(r'\s+',' ',s).strip()
    if isinstance(o,list): return [clean(x) for x in o]
    if isinstance(o,dict): return {k:clean(v) for k,v in o.items()}
    return o

def validate(slug,d,problems):
    for f in ("name","b","eta","title","meta","sub","local","nearby","faq"):
        if f not in d: problems.append(f"{slug}: missing {f}"); return False
    if len(d["local"])<4: problems.append(f"{slug}: only {len(d['local'])} local blocks")
    if len(d["faq"])<6: problems.append(f"{slug}: only {len(d['faq'])} faq")
    d["nearby"]=[[s,n] for s,n in d["nearby"] if s in VALID][:4]
    if not d["nearby"]: problems.append(f"{slug}: no valid nearby")
    txt=json.dumps(d,ensure_ascii=False)
    for w in BANNED:
        if w in txt: problems.append(f"{slug}: banned '{w}'")
    return True

def main(json_files, topup_file):
    from areas_data import AREAS
    problems=[]
    for jf in json_files:
        data=json.load(open(jf,encoding='utf-8'))
        data=clean(data)
        for slug,d in data.items():
            if slug not in VALID: problems.append(f"unknown slug {slug}"); continue
            if validate(slug,d,problems): AREAS[slug]=d
    if topup_file:
        t=clean(json.load(open(topup_file,encoding='utf-8')))
        for slug,ad in t.items():
            if slug in AREAS:
                AREAS[slug]["local"].append(ad["block"])
                AREAS[slug]["faq"].append(ad["faq"])
    import io
    out=io.StringIO(); out.write("# -*- coding: utf-8 -*-\nAREAS="); out.write(repr(AREAS))
    open('/Users/s/niv-locksmith/areas_data.py','w',encoding='utf-8').write(out.getvalue())
    print("merged:",len(AREAS),"areas | problems:",len(problems))
    for p in problems[:20]: print(" !",p)

if __name__=="__main__":
    main(sys.argv[1:-1], sys.argv[-1] if len(sys.argv)>1 else None)
