import re


def extract_price(title):

    result = {

        "price_raw" : None,
        "price_unit" : None

    }

    pattern = r"(\d+)\s*(irr|irt)"

    match = re.search(pattern, title)

    if match:

        result["price_raw"] = int(match.group(1))
        result["price_unit"] = match.group(2)

    return result