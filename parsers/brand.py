import json as js
import re

with open("/Users/mohammad/Documents/Python/projects/sepidlaptop/cleaning_prg/rules/brand_rules.json", "r", encoding="utf-8") as f:
    rules = js.load(f)

# build lookup: variant (lowercase stripped) -> canonical
_brand_map = {}
for entry in rules["brands"]:
    canonical = entry["canonical"]
    for variant in entry["variants"]:
        _brand_map[variant.lower().strip()] = canonical


def extract_brand(text):

    result = {"brand": None}

    if not isinstance(text, str) or not text.strip():
        return result

    cleaned = text.strip().lower()

    # direct lookup first
    if cleaned in _brand_map:
        result["brand"] = _brand_map[cleaned]
        return result

    # partial match — check if any variant appears in the text
    for variant, canonical in _brand_map.items():
        if re.search(re.escape(variant), cleaned):
            result["brand"] = canonical
            return result

    # fallback: return title-cased original if nothing matched
    result["brand"] = text.strip().title()
    return result