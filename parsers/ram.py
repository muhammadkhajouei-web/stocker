import re

def extract_ram(text):

    result = {
        "ram_raw_value": None,
        "ram_unit": None
    }

    if not isinstance(text, str) or not text.strip():
        return result

    # اول: عدد همراه با واحد صریح
    m = re.search(r"(\d+)\s*(gb|گیگ)\b", text, flags=re.IGNORECASE)
    if m:
        result["ram_raw_value"] = int(m.group(1))
        result["ram_unit"] = "gb"
        return result

    # دوم: عدد بدون واحد — فرض GB (رم لپ‌تاپ همیشه GB است)
    m = re.search(r"\b(\d{1,3})\b", text)
    if m:
        result["ram_raw_value"] = int(m.group(1))
        result["ram_unit"] = "gb"

    return result