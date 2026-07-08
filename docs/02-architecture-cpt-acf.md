# 02 — ארכיטקטורת CPT + ACF

עיקרון: תוכן מנוהל ב־ACF, נשמר כ־**Local JSON** (`inc/acf-json/`) כדי שיהיה תחת git ולא ידני בממשק. דורש **ACF Pro** (בגלל Flexible Content + Repeater + Clone).

---

## Custom Post Types

| CPT | slug (rewrite) | archive | תפקיד | תומך |
|-----|----------------|---------|-------|------|
| `service` | `שירותים` | כן | עמודי שירות ראשיים | title, editor, thumbnail, excerpt |
| `service_area` | `אזורי-שירות` | כן | עמודי עיר/שכונה | title, editor, thumbnail, excerpt |
| `service_area_page` | `אזורי-שירות` (משותף) | לא | שירות×אזור פרוגרמטי | title, thumbnail |
| `post` (מובנה) | `מדריכים` | כן | בלוג/מדריכים | ברירת מחדל |

עמודים רגילים (`page`): בית, אודות, קשר, נגישות, פרטיות.

### הערות רישום
- כל ה־CPT: `has_archive`, `show_in_rest: true` (בשביל עורך בלוקים + REST), `menu_icon` מתאים, `supports` לפי הטבלה.
- `service_area_page` — `has_archive: false` (הארכיון שלו הוא עמוד האזור), `rewrite` תחת `אזורי-שירות/` כדי לשמור URL אחיד.
- Rewrite slugs בעברית — לאחר רישום צריך **flush rewrite rules** (השתמש ב־hook `after_switch_theme`).

---

## Taxonomies

| taxonomy | על | תפקיד |
|----------|-----|-------|
| `service_category` | `service` | קיבוץ שירותים (פריצות / תיקונים / התקנות) — לניווט + קישור פנימי |
| `area_type` | `service_area` | סיווג: `city` / `neighborhood` / `surrounding` — לוגיקת "אזורים סמוכים" |

---

## שדות ACF — קבוצות

### א. הגדרות עסק גלובליות — `group_business_settings`
Options Page בשם "ניב · הגדרות עסק" (`acf_add_options_page`). מקור אמת לכל פרטי ה־NAP וה־CTA.

| שם שדה | key | סוג | הערה |
|--------|-----|-----|------|
| business_name | biz_name | text | "ניב המנעולן" |
| phone_display | biz_phone_display | text | `NEEDS_CLIENT_INPUT` |
| phone_e164 | biz_phone_e164 | text | ל־`tel:` — פורמט `+9725XXXXXXXX` |
| whatsapp_e164 | biz_wa | text | ל־`wa.me/` |
| email | biz_email | email | `NEEDS_CLIENT_INPUT` |
| main_city | biz_city | text | "ירושלים" |
| service_area_text | biz_area_text | text | "ירושלים והסביבה" |
| opening_hours | biz_hours | repeater(day,from,to,is_24) | `NEEDS_CLIENT_INPUT` |
| emergency_text | biz_emergency | text | "זמינים 24/7" (טעון אישור) |
| gmaps_link / waze_link | biz_gmaps / biz_waze | url | `NEEDS_CLIENT_INPUT` |
| logo | biz_logo | image | `NEEDS_CLIENT_INPUT` (קובץ לוגו) |
| cta_primary_text | biz_cta_primary | text | "חייגו עכשיו" |
| cta_secondary_text | biz_cta_secondary | text | "שלחו WhatsApp" |
| trust_badges | biz_trust | repeater(icon,label) | טקסטים מהמותג |
| license_number | biz_license | text | `NEEDS_CLIENT_INPUT` — רק אם קיים |
| police_approval_img | biz_police | image | `NEEDS_CLIENT_INPUT` — רק אם קיים |
| social_links | biz_social | repeater(network,url) | אופציונלי |
| gtm_id | biz_gtm | text | `GTM-XXXXXXX` |
| gads_conv_call / gads_conv_form | biz_gads_* | text | לייבלים מ־Google Ads |
| default_og_image | biz_og | image | ברירת מחדל לשיתוף |

### ב. Flexible Page Builder — `group_flexible_sections`
Flexible Content בשם `sections` על `page` (ואופציונלי front-page). לכל layout שדות משותפים דרך **Clone** של `group_section_common`.

**`group_section_common` (clone):** `title` (text) · `subtitle` (text) · `text` (wysiwyg) · `image` (image) · `cta_text` (text) · `cta_link` (link) · `bg_style` (select: light/stone/charcoal/red) · `enabled` (true_false, ברירת מחדל true).

**Layouts:**
`hero_emergency` · `service_cards` · `trust_badges` · `content` · `work_gallery` · `service_area_grid` · `faq_accordion` · `price_factors` · `testimonials` · `blog_preview` · `cta_strip` · `contact_form` · `map` · `internal_links` · `breadcrumb`.

לכל layout שדות ייחודיים מעבר ל־common (למשל `faq_accordion` → repeater של `q`/`a`; `price_factors` → repeater של `factor`/`impact`; `service_cards` → relationship ל־`service`).

### ג. שדות עמוד שירות — `group_service_fields` (על `service`)
`primary_keyword` · `secondary_keywords` (textarea, שורה לכל ביטוי) · `hero_title` · `hero_subtitle` · `short_desc` · `problem_desc` (wysiwyg) · `solution_desc` (wysiwyg) · `scenarios` (repeater: scenario) · `price_factors` (repeater: factor, impact) · `estimated_time_text` (רק אם סופק) · `faq` (repeater: q,a) · `related_services` (relationship→service, max 3) · `related_areas` (relationship→service_area) · `schema_service_type` (text, ברירת מחדל "Locksmith") · `seo_title` · `meta_description` · `og_image` · `canonical_url`.

### ד. שדות עמוד אזור — `group_area_fields` (על `service_area`)
`area_name` · `area_type` (select: city/neighborhood/surrounding) · `parent_area` (post_object→service_area) · `nearby_areas` (relationship→service_area) · `local_intro` (wysiwyg) · `availability_text` · `access_notes` (optional) · `services_available` (relationship→service) · `faq` (repeater: q,a) · `seo_title` · `meta_description` · `canonical_url` · `schema_area_served` (text).

### ה. שדות שירות×אזור — `group_service_area_fields` (על `service_area_page`)
`service_ref` (post_object→service, נדרש) · `area_ref` (post_object→service_area, נדרש) · `primary_keyword` · `h1` · `hero_text` · `unique_intro` (wysiwyg, **נדרש** — שער נגד thin content) · `local_context` (wysiwyg) · `service_specific` (wysiwyg) · `faq` (repeater: q,a) · `related_pages` (relationship) · `internal_links` (repeater: label,link) · `seo_title` · `meta_description` · `canonical_url` · `index_status` (select: index/noindex/draft, ברירת מחדל noindex).

---

## לוגיקת ברירות מחדל (מונעת עמודים ריקים)

- כל שדה SEO ריק → נופל לתבנית מ־`03-seo-schema.md` (למשל `{service} בירושלים | ניב המנעולן`).
- `service_area_page` עם `unique_intro` ריק → נכפה `index_status = draft` (פונקציה ב־`inc/`), לא עולה לאוויר.
- `related_*` ריק → התבנית ממלאת אוטומטית מאותה קטגוריה/אזור סמוך.

---

## מוסכמות שמות

- Field keys: `field_niv_{group}_{name}` · Group keys: `group_niv_{name}`.
- Text domain: `niv`. קידומת פונקציות: `niv_`. קידומת CSS: `.niv-`.
- כל מחרוזת גלויה עוברת `__( '...', 'niv' )` — מוכן לתרגום, אבל ברירת מחדל עברית.
