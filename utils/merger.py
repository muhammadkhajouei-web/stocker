import pandas as pd
import glob
import os

files = glob.glob("/Users/mohammad/Documents/Python/projects/sepidlaptop/clean_data/cleans/*.xlsx")
processed_list = []

for file in files:
    df = pd.read_excel(file)
    df['Origin'] = os.path.basename(file)
    processed_list.append(df)
    empty_row = pd.DataFrame([[None] * len(df.columns)], columns=df.columns)
    processed_list.append(empty_row)

final_df = pd.concat(processed_list, ignore_index=True)

cols = ['Origin'] + [c for c in final_df.columns if c != 'Origin']
final_df = final_df[cols]

final_df = final_df.replace("", pd.NA).fillna(pd.NA)

final_df.to_excel("/Users/mohammad/Documents/Python/projects/sepidlaptop/clean_data/final_6.xlsx", index=False)
print(f"فایل نهایی با موفقیت ذخیره شد. تعداد ردیف‌ها: {len(final_df)}")