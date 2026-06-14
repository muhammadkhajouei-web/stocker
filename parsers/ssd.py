import re

def extract_ssd(text):

    result = {
        "ssd_raw_value": None,
        "ssd_unit": None
    }

    if not isinstance(text, str) or not text.strip():
        return result

    # حذف پیشوندهای DDR/LPDDR که مربوط به RAM هستن نه SSD
    text = re.sub(r"\b(?:lp)?ddr\d*x?\b", "", text, flags=re.IGNORECASE).strip()

    # اول: عدد همراه با واحد صریح
    m = re.search(r"(\d+)\s*(gb|tb|گیگ|ترا)\b", text, flags=re.IGNORECASE)
    if m:
        val, unit = m.group(1), m.group(2).lower()
        if re.match(r"^(ت|t)", unit):
            result["ssd_raw_value"] = int(val) * 1024
        else:
            result["ssd_raw_value"] = int(val)
        result["ssd_unit"] = "gb"
        return result

    # دوم: عدد بدون واحد (۳ یا ۴ رقمی) — فرض GB
    m = re.search(r"\b(\d{3,4})\b", text)
    if m:
        result["ssd_raw_value"] = int(m.group(1))
        result["ssd_unit"] = "gb"

    return result