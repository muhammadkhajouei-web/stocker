import json as js
import numpy as np
import re

with open("/Users/mohammad/Documents/Python/projects/sepidlaptop/cleaning_prg/rules/gpu_rules.json", "r", encoding="utf-8") as f:
    rules = js.load(f)


def _match_rule(rule, title):
    for pattern in rule["patterns"]:
        if re.search(pattern, title, flags=re.IGNORECASE):
            return True
    return False


def _extract_vram(rule, title):
    if not rule.get("has_vram"):
        return 0, None

    vram_match = re.search(r"(\d+)\s*(gb|mb)", title, flags=re.IGNORECASE)
    if vram_match:
        return vram_match.group(1), vram_match.group(2).lower()

    return np.nan, None


def _build_result(rule, title):
    from utils.normalize import dedup

    model = None
    model_pattern = rule.get("model_pattern")
    if model_pattern:
        model_match = re.search(model_pattern, title, flags=re.IGNORECASE)
        if model_match:
            model = model_match.group().strip()

    vram, vram_unit = _extract_vram(rule, title)

    parts = [p for p in [rule["brand"], rule["family"], rule["series"], model] if p]
    if vram and vram != 0 and not (isinstance(vram, float) and np.isnan(vram)):
        parts.append(str(vram) + (vram_unit or ""))

    return {
        "gpu_brand":     rule["brand"],
        "gpu_family":    rule["family"],
        "gpu_series":    rule["series"],
        "gpu_type":      rule["default_type"],
        "gpu_model":     model,
        "gpu_vram":      vram,
        "gpu_vram_unit": vram_unit,
        "gpu_full_spec": dedup(parts),
    }


def extract_gpu_info(title):

    empty = {
        "gpu_brand": None, "gpu_family": None, "gpu_series": None,
        "gpu_type": None, "gpu_model": None, "gpu_vram": None,
        "gpu_vram_unit": None, "gpu_full_spec": None,
    }

    matched_rules = [rule for rule in rules["rules"] if _match_rule(rule, title)]

    if not matched_rules:
        return empty

    # If both Dedicated and Integrated matched, keep only Dedicated
    dedicated = [r for r in matched_rules if r["default_type"] == "Dedicated"]
    best_rule = dedicated[0] if dedicated else matched_rules[0]

    return _build_result(best_rule, title)