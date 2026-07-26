#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify a GEO product-description JSON file against the strict rules.
Usage: python3 verify_geo.py <json_path> [expected_names_json_path]
Prints all issues; exits 1 if any issue found, 0 if clean."""
import json, sys, re

BANNED = ["לסיכום", "ראשית", "שנית", "בנוסף לכך", "יתרה מזאת",
          "חשוב לציין", "במסגרת", "על מנת", "כמו כן", "יש לציין", "לאחרונה"]
DASHES = ["—", "–"]  # em dash, en dash


def wc(s):
    return len(s.split())


def check_product(name, obj, issues):
    def add(msg):
        issues.append(f"[{name}] {msg}")

    # structure
    for k in ("lead", "sections", "specs", "faq"):
        if k not in obj:
            add(f"missing key {k}")
    if any(k not in obj for k in ("lead", "sections", "specs", "faq")):
        return

    # lead
    lw = wc(obj["lead"])
    if not (40 <= lw <= 60):
        add(f"lead word count {lw} not in 40-60")

    # sections
    secs = obj["sections"]
    if len(secs) != 3:
        add(f"sections count {len(secs)} != 3")
    for i, s in enumerate(secs):
        if "h" not in s or "p" not in s:
            add(f"section {i} missing h/p")
            continue
        if ":" in s["h"] or "：" in s["h"]:
            add(f"section {i} heading has colon: {s['h']}")
        for d in DASHES:
            if d in s["h"]:
                add(f"section {i} heading has dash: {s['h']}")
        pw = wc(s["p"])
        if not (134 <= pw <= 167):
            add(f"section {i} word count {pw} not in 134-167 | h={s['h']}")

    # specs
    if not (4 <= len(obj["specs"]) <= 6):
        add(f"specs count {len(obj['specs'])} not in 4-6")

    # faq
    faq = obj["faq"]
    if len(faq) != 5:
        add(f"faq count {len(faq)} != 5")
    for i, pair in enumerate(faq):
        if not (isinstance(pair, list) and len(pair) == 2):
            add(f"faq {i} not a 2-item pair")

    # banned words + dashes over all text
    blob_parts = [obj["lead"]]
    for s in secs:
        blob_parts.append(s.get("h", ""))
        blob_parts.append(s.get("p", ""))
    blob_parts.extend(obj["specs"])
    for pair in faq:
        if isinstance(pair, list):
            blob_parts.extend([str(x) for x in pair])
    blob = " ".join(blob_parts)
    for b in BANNED:
        if b in blob:
            add(f"BANNED word present: {b}")
    for d in DASHES:
        if d in blob:
            add(f"DASH present: {repr(d)}")


def main():
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    issues = []
    for name, obj in data.items():
        check_product(name, obj, issues)

    if len(sys.argv) > 2:
        with open(sys.argv[2], encoding="utf-8") as f:
            expected = json.load(f)
        exp_names = [p["name"] for p in expected]
        for n in exp_names:
            if n not in data:
                issues.append(f"MISSING PRODUCT: {n}")
        for n in data:
            if n not in exp_names:
                issues.append(f"UNEXPECTED PRODUCT: {n}")

    if issues:
        print(f"FAIL ({len(issues)} issues):")
        for it in issues:
            print(" -", it)
        sys.exit(1)
    print(f"OK: {len(data)} products, all checks passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
