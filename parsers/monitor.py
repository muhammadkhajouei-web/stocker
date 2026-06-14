import re
import json as js
import math

with open("/Users/mohammad/Documents/Python/projects/sepidlaptop/cleaning_prg/rules/monitor_rules.json","r",encoding="utf-8") as f:
    rules = js.load(f)


def extract_monitor_info(title):
    
    result = {
        
        "monitor_screen_size" : None,
        "size_unit" : None,
        "monitor_resolution" : None,
        "monitor_refresh_rate" : None,
        "refrate_unit" : None,
        "monitor_panel_type" : None,
        "monitor_touch" : False
    }
    
    
    for rule in rules["rules"]:
        
        field = rule["field"]
        
        
        if field == "screen_size":
            
            for pattern in rule["patterns"]:
                
                unit = "inch"
            
                match = re.search(pattern, title, flags=re.IGNORECASE)
                
                if match:
                    
                    result["monitor_screen_size"] = float(match.group(1))
                    result["size_unit"] = unit
                    
                    break

            if result["monitor_screen_size"] is None:
                ppi_match = re.search(r"(\d+)\s*[x×]\s*(\d+).*?~?\s*(\d+)\s*ppi", title, re.IGNORECASE)
                if ppi_match:
                    w, h, ppi = int(ppi_match.group(1)), int(ppi_match.group(2)), int(ppi_match.group(3))
                    result["monitor_screen_size"] = round(math.sqrt(w**2 + h**2) / ppi, 1)
                    result["size_unit"] = "inch"
                    
        elif field == "resolution":
            
            for pattern in rule["patterns"]: 
                match = re.search(pattern["match"], title, flags=re.IGNORECASE)
                    
                if match:
                        
                    result["monitor_resolution"] = pattern["label"]
                        
                    break
                    
        elif field == "refresh_rate":
            
            for pattern in rule["patterns"]:
                
                unit = "hz"
                
                match = re.search(pattern, title, flags=re.IGNORECASE)
                
                if match:
                    
                    result["monitor_refresh_rate"] = int(match.group(1))
                    result["refrate_unit"] = unit
                    
                    break
        
        elif field == "panel_type":
            
            for pattern in rule["patterns"]:
                
                match = re.search(pattern["match"], title, flags=re.IGNORECASE)
                
                if match:
                    
                    result["monitor_panel_type"] = pattern["label"]
                    
                    break
                
        elif field == "is_touch":
            
            for pattern in rule["patterns"]:
                
                match = re.search(pattern, title, flags=re.IGNORECASE)
                
                if match:
                    
                    result["monitor_touch"] = True
                    
                    break
                
        
    
    return result