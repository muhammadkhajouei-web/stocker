import pandas as pd
import os


def find_empty_cells_to_txt(file_path, output_txt_path):
    # ۱. خواندن فایل اکسل
    df = pd.read_excel(file_path)

    # ۲. پیدا کردن موقعیت‌های خالی
    empty_positions = df.isna()

    # ۳. باز کردن فایل متنی برای نوشتن (w) با پشتیبانی از حروف فارسی (utf-8)
    with open(output_txt_path, "w", encoding="utf-8") as file:

        file.write("گزارش سلول‌های خالی:\n")
        file.write("-" * 30 + "\n")

        has_empty = False
        for row_idx, row in empty_positions.iterrows():
            for col_name in df.columns:
                if row[col_name]:
                    excel_row = row_idx + 2
                    # به جای print، اطلاعات را داخل فایل می‌نویسیم
                    # n\ برای این است که هر گزارش در یک خط جدید نوشته شود
                    file.write(
                        f"🔴 ردیف: {excel_row} | ستون: '{col_name}' خالی است.\n"
                    )
                    has_empty = True

        if not has_empty:
            file.write("✅ هیچ سلول خالی در فایل یافت نشد!\n")

    print(f"🎉 گزارش با موفقیت در فایل متنی ذخیره شد:\n{output_txt_path}")

'''
# آدرس فایل اکسل شما
file_name = "/Users/mohammad/Documents/Python/projects/sepidlaptop/clean_data/cleaned_laptops_check.xlsx"

# آدرس محل ذخیره فایل متنی (در همان پوشه اکسل ذخیره می‌شود)
txt_output = "/Users/mohammad/Documents/Python/projects/sepidlaptop/clean_data/empty_cells_report.txt"

# اجرای تابع
find_empty_cells_to_txt(file_name, txt_output)
'''




def find_empty_cells_to_txt_2(file_path, columns_to_ignore, output_txt_path):
    # ۱. خواندن فایل اکسل
    df = pd.read_excel(file_path)

    # ۲. حذف ستون‌هایی که می‌خواهیم نادیده گرفته شوند
    df_filtered = df.drop(columns=columns_to_ignore, errors="ignore")

    # ۳. پیدا کردن موقعیت‌های خالی
    empty_positions = df_filtered.isna()

    # ۴. باز کردن (یا ساختن) فایل متنی برای نوشتن خروجی
    # استفاده از encoding='utf-8' برای این است که حروف فارسی درست ذخیره شوند
    with open(output_txt_path, "w", encoding="utf-8") as file:

        # نوشتن هدر و توضیحات اولیه در فایل txt
        file.write("گزارش سلول‌های خالی در فایل اکسل\n")
        file.write("=" * 40 + "\n")
        file.write(f"ستون‌های نادیده گرفته شده: {columns_to_ignore}\n")
        file.write("-" * 40 + "\n\n")

        has_empty = False

        # بررسی ردیف‌ها و ستون‌ها
        for row_idx, row in empty_positions.iterrows():
            for col_name in df_filtered.columns:
                if row[col_name]:
                    excel_row = row_idx + 2
                    # به جای print، مقدار را با متد .write درون فایل می‌نویسیم
                    # n\ باعث می‌شود هر گزارش در یک خط جدید نوشته شود
                    file.write(
                        f"🔴 ردیف: {excel_row} | ستون: '{col_name}' خالی است.\n"
                    )
                    has_empty = True

        # اگر هیچ سلول خالی پیدا نشد
        if not has_empty:
            file.write("✅ هیچ سلول خالی در ستون‌های مورد نظر یافت نشد!\n")

    print(f"🎉 گزارش با موفقیت در فایل '{output_txt_path}' ذخیره شد.")

'''
# --- تنظیمات برنامه ---
excel_file = "/Users/mohammad/Documents/Python/projects/sepidlaptop/clean_data/cleaned_laptops_check.xlsx"  # نام فایل اکسل شما
ignored_cols = ["gpu_vram", "gpu_model", "gpu_full_spec","brand","model","cpu_brand","cpu_family","cpu_series","cpu_model","cpu_generation","cpu_full_spec","cpu_class","ssd_raw_value","ram_capacity"]  # ستون‌هایی که نباید بررسی شوند
txt_output = "/Users/mohammad/Documents/Python/projects/sepidlaptop/cleaning_prg/empty_reporter/empty_cells_report.txt"  # نام فایل متنی خروجی

# اجرای تابع
find_empty_cells_to_txt_2(excel_file, ignored_cols, txt_output)
'''



def extract_excel_data(file_path, row_numbers, column_names, output_txt_path):
    """تابع داینامیک برای استخراج مقادیر ردیف‌ها و ستون‌های خاص و ذخیره در فایل txt"""
    try:
        # ۱. تشخیص پسوند فایل و خواندن آن (پشتیبانی از اکسل و CSV)
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_path)
        else:
            print("❌ فرمت فایل پشتیبانی نمی‌شود! لطفا فایل Excel یا CSV بدهید.")
            return

        # ۲. تبدیل ورودی‌ها به لیست (اگر به صورت تکی وارد شده باشند)
        if not isinstance(row_numbers, list):
            row_numbers = [row_numbers]
        if not isinstance(column_names, list):
            column_names = [column_names]

        # ۳. بررسی وجود ستون‌های درخواستی در فایل
        missing_cols = [col for col in column_names if col not in df.columns]
        if missing_cols:
            print(f"❌ این ستون‌ها در فایل پیدا نشدند: {missing_cols}")
            print(f"ستون‌های موجود در فایل شما: {list(df.columns)}")
            return

        # ۴. باز کردن فایل متنی خروجی
        with open(output_txt_path, "w", encoding="utf-8") as file:
            for row in row_numbers:
                # تبدیل شماره ردیف اکسل به ایندکس پایتون
                # ردیف ۱ هدر است، پس ردیف ۲ اکسل می‌شود ایندکس ۰ در پانداز
                pyd_idx = row - 2

                # بررسی اینکه شماره ردیف وارد شده در محدوده فایل باشد
                if pyd_idx < 0 or pyd_idx >= len(df):
                    file.write(
                        f"⚠️ ردیف {row}: این شماره ردیف در محدوده فایل وجود ندارد.\n"
                    )
                    continue

                # استخراج مقادیر ستون‌های درخواستی برای این ردیف
                for col in column_names:
                    value = df.at[pyd_idx, col]
                    # نوشتن در فایل متنی
                    file.write(f"{value}\n")

        print(f"🎉 مقادیر با موفقیت در فایل زیر ذخیره شد:\n{output_txt_path}")

    except Exception as e:
        print(f"❌ خطایی رخ داد: {e}")


# ========================================================
# بخش تنظیمات داینامیک (مقادیر خود را اینجا وارد کنید)
# ========================================================

# ۱. آدرس فایل ورودی (می‌تواند xlsx یا csv باشد)
input_file = "/Users/mohammad/Documents/Python/projects/sepidlaptop/input_data/goldkala_laptops.csv"

# ۲. لیست شماره ردیف‌های مورد نظر (دقیقاً همان شماره‌ای که در اکسل می‌بینید)
rows_to_extract = [
    5, 6, 7, 14, 34, 35, 36, 43, 44, 45, 57, 63, 91, 92, 93, 98, 99, 100, 101,
    117, 118, 119, 120, 121, 122, 123, 124, 128, 139, 140, 153, 154, 156, 172,
    175, 176, 178, 179, 180, 181, 183, 184, 190, 194, 204, 207, 235, 237, 238,
    239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253,
    255, 256, 257, 258, 260, 261, 262, 263, 264, 265, 266, 267, 268, 272, 273,
    274, 275, 276, 297, 298, 315, 321, 322, 334, 343, 358, 359, 360, 361, 362,
    363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 376, 377, 378,
    379, 381, 391, 406, 407, 408, 409, 410, 411, 412, 417, 423, 424
]

# ۳. نام ستون یا ستون‌هایی که مقادیرشان را می‌خواهید
columns_to_extract = "گرافیک"

# ۴. مسیر فایل متنی خروجی
output_file = "/Users/mohammad/Documents/Python/projects/sepidlaptop/cleaning_prg/empty_reporter/extracted_values.txt"

# اجرای برنامه
extract_excel_data(input_file, rows_to_extract, columns_to_extract, output_file)










