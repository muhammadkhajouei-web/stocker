import json as js
import re
from utils.normalize import dedup


with open("/Users/mohammad/Documents/Python/projects/sepidlaptop/cleaning_prg/rules/cpu_rules.json", "r", encoding="utf-8") as f:
    rules = js.load(f)
    
    
def extract_cpu_info(title, full_spec=None):

    # اگر ستون پردازنده خالی بود، full_spec رو normalize کرده و به عنوان منبع اصلی امتحان کن
    if (not title or not title.strip()) and full_spec:
        from utils.normalize import normalize_cpu
        title = normalize_cpu(full_spec)
    
    result = {
        
        "cpu_brand": None,
        "cpu_family": None,
        "cpu_series": None,
        "cpu_model":None,
        "cpu_generation":None,
        "cpu_suffix": None,
        "cpu_full_spec":None,
        "cpu_class": None
    }
    
    
    for rule in rules["rules"]:
        for pattern in rule["patterns"]:
            match = re.search(pattern, title, flags=re.IGNORECASE)
               
            if match:
                result.update({
                        "cpu_brand" : rule["brand"].lower(),
                        "cpu_family": rule["family"].lower(),
                        "cpu_series": rule["series"].lower(),
                        "cpu_class": rule["class"].lower()
                    })
                cpu_model_match = re.search(rule["model_pattern"], match.group(), flags=re.IGNORECASE)       
                    
                if cpu_model_match:
                    result["cpu_model"] = cpu_model_match.group(1).lower()
                    _suffix_match = re.search(r'(hx|hs|hq|h|u|g\d|p|y|m)$', result["cpu_model"], re.IGNORECASE)
                    result["cpu_suffix"] = _suffix_match.group(1).upper() if _suffix_match else None
                    
                    if rule["generation_method"] in ["intel_core", "intel_ultra", "amd_ryzen"]:
                    
                        model_nums = re.search(r"^\d+", cpu_model_match.group(1))  
                         
                        if model_nums:
                            clean_nums = model_nums.group()
                            model_nums_len = len(clean_nums)
                        
                            if model_nums_len == 5:
                                result["cpu_generation"] = int(clean_nums[:2])
                                
                            elif model_nums_len == 4:
                        
                                if clean_nums.startswith(('10','11','12','13','14')):
                                    result["cpu_generation"] = int(clean_nums[:2])
                                
                                else:
                                    result["cpu_generation"] = int(clean_nums[:1])
                                    
                            elif model_nums_len == 3:
                                result["cpu_generation"] = int(clean_nums[:1])
                                
                            elif model_nums_len == 2 :
                                result["cpu_generation"] = int(clean_nums)

                    elif rule["generation_method"] == "prefix_map" and "generation_map" in rule:

                        model_nums = re.search(r"^\d+", cpu_model_match.group(1))

                        if model_nums:
                            clean_nums = model_nums.group()
                            result["cpu_generation"] = next((entry["generation"] for entry in rule["generation_map"] if clean_nums.startswith(entry["prefix"])), None)

                    elif rule["generation_method"] == "snapdragon":
                        model_str = cpu_model_match.group(1)

                        m = re.search(r"gen\s*(\d)", model_str, re.IGNORECASE)

                        if m:
                            result["cpu_generation"] = int(m.group(1))

                        else:
                            mx = re.search(r"\bx(\d)\b", model_str, re.IGNORECASE)

                            if mx:
                                result["cpu_generation"] = int(mx.group(1))
                            elif re.search(r"\bx\b", model_str, re.IGNORECASE):
                                result["cpu_generation"] = 1
                            else:
                                result["cpu_generation"] = None

                    else:
                        result["cpu_generation"] = None
                    
                else:
                    result["cpu_model"] = None
                    result["cpu_generation"] = None

                if result["cpu_generation"] is None:
                    gen_fallback = re.search(r"\bgen(\d+)\b", title, re.IGNORECASE)
                    if gen_fallback:
                        result["cpu_generation"] = int(gen_fallback.group(1))

                if result["cpu_generation"] is None and result["cpu_brand"] == "intel":
                    macbook_intel_gen_map = {
                        2015: 5, 2016: 6, 2017: 7,
                        2018: 8, 2019: 9, 2020: 10, 2021: 10
                    }
                    for source in [title, full_spec]:
                        if source and result["cpu_generation"] is None:
                            m = re.search(r"\bmacbook\b.*?\b(20\d{2})\b|\b(20\d{2})\b.*?\bmacbook\b", source, re.IGNORECASE)
                            if m:
                                year = int(m.group(1) or m.group(2))
                                result["cpu_generation"] = macbook_intel_gen_map.get(year)

                if result["cpu_brand"] == "apple" and result["cpu_model"]:
                    mac_variant = None
                    for source in [title, full_spec]:
                        if source and mac_variant is None:
                            m = re.search(r"\bmacbook\s*(pro|air)\b", source, re.IGNORECASE)
                            if m:
                                mac_variant = m.group(1).lower()
                    if mac_variant and mac_variant not in result["cpu_model"]:
                        result["cpu_model"] = result["cpu_model"] + " " + mac_variant

                parts = [rule["brand"], rule["family"], rule["series"]]
                if result["cpu_model"]:
                    parts.append(result["cpu_model"])

                result["cpu_full_spec"] = dedup(parts)

                return result
                  
    return result