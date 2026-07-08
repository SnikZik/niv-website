# 04 — תוכנית מדידה, dataLayer ו־GTM

**חשוב:** ל־LP הקיים כבר יש GTM + המרות Google Ads. **לא לדרוס קונפיגורציה קיימת.** GTM מוזרק פעם אחת בלבד (מ־Business Settings `biz_gtm`), עם בדיקה שהוא לא כבר בעמוד.

עיקרון: התמה יורה `dataLayer.push` אחיד; GTM מתרגם ל־tags/triggers; חלק מה־triggers מחוברים להמרות Google Ads. הקוד לא מכיר את מזהי ההמרה — הם חיים ב־GTM/ACF.

---

## data-attributes על כל אלמנט CTA (מקור האמת ל־GTM)

כל כפתור/קישור פעולה נושא:

```html
<a class="niv-btn niv-btn--call js-call-click"
   href="tel:+9725XXXXXXXX"
   data-cta-location="hero"     <!-- header / hero / sticky / section-x / footer -->
   data-service="החלפת צילינדר" <!-- ריק בעמודים כלליים -->
   data-area="גבעת זאב"         <!-- ריק בעמודים כלליים -->
   aria-label="חייגו לניב המנעולן">חייגו עכשיו</a>
```

Classes: `.js-call-click` · `.js-whatsapp-click` · `.js-sticky-cta` · `.js-service-card` · `.js-area-card` · `.js-form` (על ה־`<form>`).

`data-service` / `data-area` מוזרקים אוטומטית מהתבנית לפי סוג העמוד הנוכחי.

---

## אירועי dataLayer

| event | trigger | פרמטרים |
|-------|---------|---------|
| `click_to_call` | קליק על כל `tel:` / `.js-call-click` | page_url, page_title, cta_location, phone_number, service, area |
| `whatsapp_click` | קליק על `.js-whatsapp-click` | page_url, page_title, cta_location, service, area |
| `lead_form_start` | אינטראקציה ראשונה עם טופס | page_url, form_id |
| `lead_form_submit` | שליחה מוצלחת | page_url, form_id, service, area |
| `lead_form_error` | שגיאת ולידציה | page_url, form_id, error_type |
| `service_area_click` | קליק מגריד אזורים | area_name, source_page |
| `service_click` | קליק מכרטיסי שירות | service_name, source_page |
| `sticky_cta_click` | קליק ב־CTA דביק בנייד | cta_type (call/whatsapp), page_url |

מימוש: `assets/js/tracking.js` — delegation יחיד על `document` (עמיד ל־DOM דינמי), `window.dataLayer = window.dataLayer || []` לפני כל push.

---

## חיבור להמרות Google Ads (למתעד ה־GTM)

| המרה | GTM Trigger | הערה |
|------|-------------|------|
| **Call (עיקרי)** | Custom Event = `click_to_call` | ההמרה החשובה ביותר לעסק חירום |
| **WhatsApp** | Custom Event = `whatsapp_click` | להגדיר כ־secondary conversion |
| **Lead form** | Custom Event = `lead_form_submit` | להעביר service/area כ־parameters |

- לייבלים של Google Ads נשמרים ב־ACF (`biz_gads_conv_call`, `biz_gads_conv_form`) ומוזנים ב־GTM, לא בקוד.
- להגדיר Trigger Group אם רוצים לספור call+whatsapp כ־"פנייה".
- GA4: אותם אירועים נשלחים אוטומטית כ־GA4 events דרך GTM (מומלץ לסמן `click_to_call`, `whatsapp_click`, `lead_form_submit` כ־Key Events).

---

## QA מדידה (לפני launch)
- GTM Preview: כל 8 האירועים נורים עם הפרמטרים הנכונים.
- click_to_call יורה בנייד אמיתי (לא רק דסקטופ).
- GTM מוזרק **פעם אחת** (בדיקת View Source).
- אין כפילות עם ה־LP הישן אם חולקים אותו container.
