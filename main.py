import pandas as pd
from parsers import extract_cpu_info, extract_ssd, extract_ram, extract_gpu_info, extract_monitor_info, extract_price
from parsers.brand import extract_brand
from utils.normalize import normalize_cpu, normalize_ssd_ram, normalize_gpu, normalize_monitor, normlize_price

path = "/Users/mohammad/Documents/Python/projects/sepidlaptop/input_data/300recs.csv"

rawdata = pd.read_csv(path)

pd.set_option("display.max_rows", None)

cleandf = pd.DataFrame()


def brand_ext():

    brand_df = rawdata["برند"].apply(extract_brand).apply(pd.Series)

    for col in brand_df.columns:
        cleandf[col] = brand_df[col]


def cpu_ext():

    cpu_clean_series = rawdata["سی پی یو"].apply(normalize_cpu)
    full_spec_series = rawdata["شرح"]

    cpu_df = pd.DataFrame([
        extract_cpu_info(cpu, full_spec)
        for cpu, full_spec in zip(cpu_clean_series, full_spec_series)
    ])

    for col in cpu_df.columns:
        cleandf[col] = cpu_df[col]


def ssd_ext():

    ssd_clean_series = rawdata["هارد"].apply(normalize_ssd_ram)

    ssd_df = ssd_clean_series.apply(extract_ssd).apply(pd.Series)

    for col in ssd_df.columns:
        cleandf[col] = ssd_df[col]


def ram_ext():

    ram_clean_series = rawdata["رم"].apply(normalize_ssd_ram)

    ram_df = ram_clean_series.apply(extract_ram).apply(pd.Series)

    for col in ram_df.columns:
        cleandf[col] = ram_df[col]


def gpu_ext():

    gpu_clean_series = rawdata["گرافیک"].apply(normalize_gpu)

    gpu_df = gpu_clean_series.apply(extract_gpu_info).apply(pd.Series)

    for col in gpu_df.columns:
        cleandf[col] = gpu_df[col]


def monitor_ext():

    monitor_clean_series = rawdata["مانیتور"].apply(normalize_monitor)

    monitor_df = monitor_clean_series.apply(extract_monitor_info).apply(pd.Series)

    for col in monitor_df.columns:
        cleandf[col] = monitor_df[col]


def price_ext():

    price_clean_series = rawdata["قیمت"].apply(normlize_price)

    price_df = price_clean_series.apply(extract_price).apply(pd.Series)

    for col in price_df.columns:
        cleandf[col] = price_df[col]


def link_ext():

    cleandf["product_link"] = rawdata["لینک"]


def main():

    brand_ext()
    cpu_ext()
    ssd_ext()
    ram_ext()
    gpu_ext()
    monitor_ext()
    price_ext()
    link_ext()

    clean_output_path = "/Users/mohammad/Documents/Python/projects/sepidlaptop/clean_data/cleans/300recs.xlsx"

    cleandf.to_excel(clean_output_path, index=False, engine="openpyxl")
    print(f"فایل اکسل با موفقیت در این مسیر ذخیره شد:\n{clean_output_path}")


main()