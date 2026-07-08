# 03 — SEO: תבניות meta + סכמות + חוקי תוכן

מנוע SEO: **Yoast** או **Rank Math** לניהול title/meta ו־sitemap. הסכמות (JSON-LD) מוזרקות מהתמה (`inc/schema.php`) כדי לשלוט מלא ולקשר ל־ACF. אם משתמשים ב־Yoast — לכבות את סכמת ה־Article/LocalBusiness שלו כדי למנוע כפילות, או להיפך: לתת ל־Yoast לנהל ולכבות את שלנו. **מקור סכמה אחד בלבד לכל סוג.**

---

## תבניות SEO Title

| עמוד | תבנית | תווים יעד |
|------|-------|-----------|
| בית | `מנעולן לדלתות בירושלים | ניב המנעולן` | 55–60 |
| שירות | `{service} בירושלים | ניב המנעולן` | 55–60 |
| אזור | `מנעולן ב{area} | שירות לדלתות וצילינדרים` | 55–60 |
| שירות×אזור | `{service} ב{area} | ניב המנעולן` | 55–60 |
| מדריך | `{title} | מדריך מנעולנות בירושלים` | 55–60 |

## תבניות Meta Description (ייחודי לכל עמוד לפני פרסום!)

- **בית:** צריכים מנעולן לדלתות בירושלים? ניב המנעולן מספק מענה לדלתות, צילינדרים, מנגנונים ותקלות נעילה באזור ירושלים. התקשרו לקבלת מענה מהיר.
- **שירות:** צריכים {service} בירושלים? ניב המנעולן מספק שירות מקצועי לדלתות, צילינדרים ומנגנונים עם הסבר ברור לפני העבודה. חייגו עכשיו.
- **אזור:** מחפשים מנעולן ב{area}? ניב המנעולן נותן מענה לדלתות, צילינדרים ותקלות נעילה באזור {area} והסביבה. התקשרו עכשיו.
- **שירות×אזור:** צריכים {service} ב{area}? ניב המנעולן מספק מענה מהיר וברור לתקלות דלתות ומנעולים באזור {area}. חייגו לקבלת פרטים.

> אורך יעד 130–145 תווים. הפונקציה `niv_meta_description()` מקצרת/מרחיבה חכם ומזהירה בלוג אם חורג.

---

## סכמות JSON-LD (inc/schema.php)

| טיפוס | היכן | מקור נתונים |
|-------|------|-------------|
| `Locksmith` (subtype של LocalBusiness) | כל עמוד (Organization+NAP) | Business Settings |
| `WebSite` + `SearchAction` | בית | קבוע |
| `Service` | עמוד שירות + שירות×אזור | ACF service fields, `areaServed` |
| `FAQPage` | רק כשה־FAQ **מוצג** בעמוד | ACF faq repeater |
| `BreadcrumbList` | כל עמוד פנימי | היררכיית העמוד |
| `Review` / `AggregateRating` | ⚠️ **רק אם יש ביקורות אמת מאומתות** | `NEEDS_CLIENT_INPUT` |

### Locksmith schema — שדות ליבה
`name, image, url, telephone, email, address (PostalArea/ירושלים), areaServed[], geo, openingHoursSpecification, priceRange` — כולם מ־Business Settings. אם `opening_hours` = 24/7 → `opens 00:00 closes 23:59` לכל יום (רק אם אושר).

> **אין AggregateRating מזויף.** בלי דירוג אמת → אין כוכבים ב־SERP. עדיף אמת.

---

## חוקי תוכן ואיכות (מונע עונשי SEO)

- **H1 אחד** לכל עמוד, מכיל את מילת המפתח באופן טבעי.
- H2/H3 בהיררכיה נכונה, מילת מפתח ב־2+ כותרות H2.
- מילת מפתח ב־100 המילים הראשונות + בצפיפות טבעית (בלי stuffing).
- **מינימום 750 מילים** לעמוד שירות/אזור עיקרי; שירות×אזור ≥ 400 מילים ייחודיות.
- **אין פסקאות כפולות** בין עמודים. כל שירות×אזור עם `unique_intro` + `local_context` ייחודיים.
- עמוד ללא תוכן ייחודי מספק → `noindex` + draft (נאכף אוטומטית).
- alt לכל תמונה משמעותית; alt ריק לדקורטיבית.
- קישור פנימי לפי `08-content-plan.md` — אין עמודים יתומים.
- כל title ו־meta **ייחודיים** — פונקציית QA סורקת כפילויות לפני launch.

---

## Open Graph / Twitter
`og:title, og:description, og:image (biz_og fallback), og:type, og:url, og:locale=he_IL` + `twitter:card=summary_large_image`. מוזרק ב־`inc/seo.php` אם Yoast לא מנהל.

## טכני
- Sitemap XML דרך Yoast/Rank Math (כולל CPTs, מחריג noindex).
- `robots.txt`: לאפשר הכל חוץ מ־`/wp-admin/` (מלבד admin-ajax), להצביע על ה־sitemap.
- Canonical עצמי לכל עמוד; שירות×אזור canonical עצמי רק אם index.
- Core Web Vitals: ראה `05` + `07`.
