# -*- coding: utf-8 -*-
# Single source of truth for the business JSON-LD entity (Locksmith LocalBusiness + Person).
# Imported by all generators so every page carries the same comprehensive, consistent schema.
from areas_data import AREAS

BASE = 'https://nivlocksmith.co.il'

# separate municipalities (real cities) vs Jerusalem neighborhoods (places)
_CITIES = {'manulan-givat-zeev','manulan-mevaseret','manulan-maale-adumim',
           'manulan-abu-gosh','manulan-motza','manulan-tzur-hadassah'}

def _areas_served():
    served = [{"@type": "City", "name": "ירושלים"}]
    for slug, v in AREAS.items():
        nm = v.get('name') or v.get('b') or slug
        if slug in _CITIES:
            served.append({"@type": "City", "name": nm})
        else:
            served.append({"@type": "Place", "name": f"{nm}, ירושלים"})
    return served

# service catalog with "starting from" prices (matches the מחירון)
_OFFERS = [
    ("פריצת דלת", 350), ("החלפת צילינדר", 350), ("תיקון דלתות", 350),
    ("החלפת ידיות", 250), ("התקנת מנעול מכני לדלת", 650), ("התקנת דלת ממ״ד", 650),
    ("תיקון דלת ממ״ד", 350), ("פריצת כספות", 350), ("התקנת כספת כולל הכספת", 550),
    ("התקנת מנעול חכם כולל המנעול", 2200), ("התקנת מנעול חכם", 500),
]
def _offer_catalog():
    items = []
    for name, price in _OFFERS:
        items.append({
            "@type": "Offer",
            "itemOffered": {"@type": "Service", "name": name, "provider": {"@id": BASE + "/#business"}},
            "priceSpecification": {"@type": "PriceSpecification", "priceCurrency": "ILS", "minPrice": price},
            "priceCurrency": "ILS",
        })
    return {"@type": "OfferCatalog", "name": "שירותי מנעולן בירושלים", "itemListElement": items}

# Person node — Niv, the locksmith himself
PERSON = {
    "@type": "Person",
    "@id": BASE + "/#niv",
    "name": "ניב",
    "jobTitle": "מנעולן",
    "worksFor": {"@id": BASE + "/#business"},
    "url": BASE + "/odot.html",
    "image": BASE + "/img/niv/niv-portrait.jpg",
}

# Locksmith LocalBusiness node — the full business entity
BIZ = {
    "@type": "Locksmith",
    "@id": BASE + "/#business",
    "name": "ניב המנעולן",
    "alternateName": "ניב מנעולן בירושלים",
    "description": ("מנעולן מקצועי בירושלים והסביבה, זמין 24/7 לפריצת דלתות, החלפת צילינדרים, "
                    "תיקון דלתות, דלתות ממ״ד, כספות ומנעולים חכמים. ניב מגיע בעצמו תוך כ-20 דקות, "
                    "מחיר סגור מראש בטלפון, בלי מוקד ובלי קבלני משנה."),
    "url": BASE + "/",
    "telephone": "+972508307269",
    "image": BASE + "/logo.png",
    "logo": BASE + "/logo.png",
    "priceRange": "₪₪",
    "currenciesAccepted": "ILS",
    "paymentAccepted": "מזומן, כרטיס אשראי, ביט, העברה בנקאית",
    "address": {"@type": "PostalAddress", "addressLocality": "ירושלים",
                "addressRegion": "ירושלים", "addressCountry": "IL"},
    "geo": {"@type": "GeoCoordinates", "latitude": 31.7683, "longitude": 35.2137},
    "hasMap": "https://www.google.com/maps?q=%D7%99%D7%A8%D7%95%D7%A9%D7%9C%D7%99%D7%9D",
    "areaServed": _areas_served(),
    "openingHoursSpecification": {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "opens": "00:00", "closes": "23:59",
    },
    "founder": {"@id": BASE + "/#niv"},
    "employee": {"@id": BASE + "/#niv"},
    "knowsAbout": ["פריצת דלתות", "החלפת צילינדר", "תיקון דלתות", "דלת ממ״ד",
                   "מנעול חכם", "פריצת כספות", "דלת פלדלת", "מנעולן חירום", "מנעול רב בריח"],
    "slogan": "מנעולן שמגיע בעצמו, תוך כ-20 דקות, עם מחיר סגור מראש",
    "hasOfferCatalog": _offer_catalog(),
}

# convenience: the two entity nodes to prepend to any @graph
def biz_nodes():
    return [BIZ, PERSON]
