# GEO-ANALYSIS — ניב המנעולן (nivlocksmith.co.il)

תאריך: 2026-07-27 · אחרי סבב אופטימיזציה מקיף SEO / GEO / AIO

## GEO Readiness Score: 88/100

| קטגוריה | ציון | סטטוס |
|---|---|---|
| Technical Accessibility (SSR + crawlers) | 20/20 | HTML סטטי = 100% server-rendered, כל התוכן זמין לקראולרים בלי JS |
| Structural Readability | 18/20 | H1→H2→H3 נקי, כותרות שאלה ב-425 עמודים, FAQ פתוח, טבלאות מחירים |
| Citability (134-167w blocks) | 16/20 | בלוקי תשובה ישירה, מחיר/זמן הגעה מפורשים; אפשר להוסיף עוד בלוקים ציטוטיים |
| Authority & Brand Signals | 15/20 | Person(ניב)+תעודה+ביקורות לקוחות אמיתיות · **חוסר: נוכחות off-site** (ר' למטה) |
| Multi-Modal | 19/20 | וידאו אמיתי, תמונות עבודה, פוסטרים, לוגו — עם schema תומך |

## Platform breakdown
- **Google AI Overviews:** חזק — schema LocalBusiness מלא + SSR + local. עיקר החשיפה תלוי בדירוג האורגני המקומי.
- **ChatGPT / Perplexity:** בינוני — התוכן והישות מוכנים, אבל ציטוט תלוי ב-mentions ב-Reddit/Wikipedia/YouTube (חסר, ר' המלצות).
- **Bing Copilot:** מוכן — schema + sitemap; מומלץ IndexNow.

## AI Crawler Access — ✅ פתוח
robots.txt מאשר GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot (+ ChatGPT-User). אין חסימת JS (סטטי).

## llms.txt — ✅ קיים
`/llms.txt` (95 שורות) עם מבנה עמודים + עובדות מפתח, על הדומיין החדש.

## Schema (JSON-LD) — ✅ מקיף, בכל 504 העמודים
- **Locksmith (LocalBusiness):** 33 areaServed (כל שכונות ירושלים + גבעת זאב/מבשרת/מעלה אדומים/אבו גוש/מוצא/צור הדסה), geo (31.7683,35.2137), openingHours 24/7, priceRange, address, currency/payment, hasMap, knowsAbout, slogan, description.
- **Person (ניב):** founder + employee, jobTitle מנעולן, מקושר ב-@id, תמונה.
- **hasOfferCatalog:** 11 שירותים עם minPrice (תואם מחירון: פריצה 350, צילינדר 350, ידיות 250, תיקון 350, מנעול מכני 650, ממ״ד 650/350, כספות 350/550, מנעול חכם 2200/500).
- **לכל עמוד:** Service + FAQPage (493 עמודים) + BreadcrumbList. בית: WebSite + FAQPage.
- 672 בלוקי JSON-LD — כולם תקינים (0 שגיאות). מקור אחד: `schema_business.py`.

## Open Graph + Twitter — ✅ בכל 504 העמודים
og:type/title/description/url/image/site_name/locale + twitter card. תמונת שיתוף: ניב בעבודה.

## Meta / "Yoast"
title 48-60 תווים, description ~130-146, canonical לדומיין החדש, favicon — בכל עמוד. sitemap.xml = 236 URLs חיים (268 מדורגים noindex, 10/שבוע).

## Top 5 שינויים שבוצעו
1. Schema LocalBusiness מקיף (אזורים/שעות/ניב/geo/קטלוג) על כל האתר — היה מינימלי (4 ערים).
2. Person(ניב) + founder — זהות בעל העסק ל-AI/Knowledge Graph.
3. hasOfferCatalog עם מחירים — מאותת שירותים+תמחור ל-AI.
4. OG/Twitter site-wide — היה חסר לגמרי.
5. איחוד מקור סכמה (`schema_business.py`) — עקביות ואפס כפילויות @id.

## המלצות להמשך (בעיקר off-site — המנוף הכי חזק ל-GEO)
> Brand mentions מנבאים חשיפת AI פי 3 מ-backlinks.
1. **Google Business Profile** — קריטי ל-local + AI. ליצור/לאמת, לקשר ב-sameAs.
2. **מ-mentions:** פרופיל + פעילות ב-Facebook/Instagram עסקי, מדריך/סרטונים ב-YouTube, מענה בפורומים מקומיים.
3. **sameAs בסכמה** — להוסיף קישורי GBP + רשתות ברגע שקיימים.
4. **ביקורות Google אמיתיות** — לאסוף; אז אפשר aggregateRating אמיתי (לא ממציאים).
5. **IndexNow** ל-Bing + הגשת sitemap ל-GSC / Bing Webmaster (אחרי go-live).

## תלוי בהשלמת פרודקשן
הגשת sitemap ל-Google Search Console + Bing — ברגע ש-nivlocksmith.co.il חי (DNS מתפשט). `inject_tracking.py` מוכן ל-GA4/GSC ברגע שתהיה מזהה.

## תשתית (למפתח)
`schema_business.py` = מקור אמת לישות העסק. `inject_schema.py` = post-process (BIZ+OG) — **חובה להריץ אחרי כל regen**, לפני `apply_staging.py`. סדר פייפליין: generators → fix_prices → fix_header → inject_schema → apply_staging → deploy.
