import re
import pandas as pd

def normalize_cpu(text):
    
    if not text or pd.isna(text):
        return ""
    
    
    text = str(text).lower()
    text = re.sub(r'[®™©]', '', text)

    
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    arabic_digits = "٠١٢٣٤٥٦٧٨٩"
    english_digits = "0123456789"
    
    for i in range(10):
        
        text = text.replace(persian_digits[i], english_digits[i])
        text = text.replace(arabic_digits[i], english_digits[i])

    text = re.sub(r'[\u2010\u2011\u2012\u2013\u2014\u2015\u2212]', '-', text)

    persian_ordinals = {
        "اول": "1", "دوم": "2", "سوم": "3", "چهارم": "4", "پنجم": "5",
        "ششم": "6", "هفتم": "7", "هشتم": "8", "نهم": "9", "دهم": "10",
        "یازدهم": "11", "دوازدهم": "12", "سیزدهم": "13", "چهاردهم": "14"
    }
    for ordinal, num in persian_ordinals.items():
        text = re.sub(rf"(نسل\s*){ordinal}", rf"\g<1>{num}", text)

    persian_gen_match = re.search(r"نسل\s*([\u06F0-\u06F9]+|\d+)", text)
    if persian_gen_match:
        gen_num_str = persian_gen_match.group(1)
        for i in range(10):
            gen_num_str = gen_num_str.replace(persian_digits[i], english_digits[i])
            gen_num_str = gen_num_str.replace(arabic_digits[i], english_digits[i])
        text = text + " gen" + gen_num_str

    text = re.sub(r"[\u0600-\u06FF]+", " ", text)
    
    text = re.sub(r"[-_/_|\(\)\[\]\+\?\!\u2010\u2011\u2013\u2014]", " ", text)
    
    if not re.search(r'\bmacbook\b', text):
        text = re.sub(r"\b(20[0-2][0-9])\b", " ", text)
    
    text = re.sub(r'\s+', ' ', text)
    
    text = text.strip()
    
    return text


def normalize_ssd_ram(text):
    
    if not text or pd.isna(text):
        return ""
    
    text = str(text).lower()

    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    arabic_digits = "٠١٢٣٤٥٦٧٨٩"
    english_digits = "0123456789"
    
    for i in range(10):
        
        text = text.replace(persian_digits[i], english_digits[i])
        text = text.replace(arabic_digits[i], english_digits[i])

    text = re.sub(r'[\u2010\u2011\u2012\u2013\u2014\u2015\u2212]', '-', text)

    text = re.sub(r"[-_/_|\(\)\[\]\+\?\!]", " ", text)
    
    text = re.sub(r'\s+', ' ', text)
    
    text = text.strip()
    
    return text


def normalize_gpu(text):
    
    if not text or pd.isna(text):
        return ""
    
    text = str(text).lower()
    text = re.sub(r'[®™©]', '', text)

    
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    arabic_digits = "٠١٢٣٤٥٦٧٨٩"
    english_digits = "0123456789"
    
    for i in range(10):
        text = text.replace(persian_digits[i], english_digits[i])
        text = text.replace(arabic_digits[i], english_digits[i])
    
    capa_words = {
        "gb": ["گیگابایت", "گیگ", "gb"],
        "mb": ["مگابایت", "مگ", "mb"]
    }
    for unit, pars in capa_words.items():
        for p in pars:
            text = text.replace(p, unit)

    text = re.sub(r'[\u2010\u2011\u2012\u2013\u2014\u2015\u2212]', '-', text)

    text = re.sub(r"[-_/_|\\(\)\[\]\+\?\!\\@\\#\\*\\.\\,]", " ", text)
    
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

  
def normalize_monitor(text):
    
    if not text or pd.isna(text):
        return ""
    
    text = str(text).lower()
    text = re.sub(r'[®™©]', '', text)

    
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    arabic_digits = "٠١٢٣٤٥٦٧٨٩"
    english_digits = "0123456789"
    
    for i in range(10):
        text = text.replace(persian_digits[i], english_digits[i])
        text = text.replace(arabic_digits[i], english_digits[i])

    text = re.sub(r'[\u2010\u2011\u2012\u2013\u2014\u2015\u2212]', '-', text)

    # تبدیل علامت ضرب یونیکد به x و حذف کاما از اعداد (مثل ۲,۴۹۶ → 2496)
    text = re.sub(r'[\u00d7\u00d8\u2715\u2716]', 'x', text)
    text = re.sub(r'(\d),(\d)', r'\1\2', text)

    text = text.replace("اینچ", "inch")
    
    text = re.sub(r"[-_/_|\\(\)\[\]\+\?\!\\@\\#\\*\\,]", " ", text)
    
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def normlize_price(text):
    
    if not text or pd.isna(text):
        return ""
    
    text = str(text).lower()
    
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    arabic_digits = "٠١٢٣٤٥٦٧٨٩"
    english_digits = "0123456789"
    
    for i in range(10):
        text = text.replace(persian_digits[i], english_digits[i])
        text = text.replace(arabic_digits[i], english_digits[i])
        
    units = {
        "irr": "\u0631\u06cc\u0627\u0644",
        "irt": "تومان"
    }

    for unit, par in units.items():
        text = text.replace(par, unit)

    text = re.sub(r"[-_/_|\\(\)\[\]\+\?\!\\@\\#\\*\\,،٬]", "", text)

    text = re.sub(r'\s+', ' ', text)

    return text.strip()


    
def dedup(parts):

    result = []

    for token in parts:
        t = token.lower()

        if not any(t in r.lower() or r.lower() in t for r in result):
            result.append(t)

    return " ".join(result)