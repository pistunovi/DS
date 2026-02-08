# Розрахуємо статистичні характеристики кожної акції
#Ми обчислюємо для кожної компанії:
#•	середню ціну закриття (mean)
#•	стандартне відхилення (std)
#•	мінімум/максимум (min/max)
#•	середню денну дохідність (Daily_Return)
#•	всі дані будуть братися з файлу Excel а результати розрахунків – записуватися в інші файли Excel.

import pandas as pd
# Завантаження очищеної таблиці
file_path = r"D:\A1\stocks_parsing_part1_with_returns_cleaned.xlsx"
df = pd.read_excel(file_path)
# Групування по компанії
stats_df = df.groupby("Company").agg({
    "Close": ["mean", "std", "min", "max"],
    "Daily_Return": ["mean", "std", "min", "max"]
}).reset_index()
# Об’єднуємо мультиіндекс колонок у прості
stats_df.columns = ['_'.join(col).strip('_') for col in stats_df.columns.values]
# Збереження у Excel
stats_file = r"D:\A1\stocks_statistics.xlsx"
stats_df.to_excel(stats_file, index=False)
print("Статистичні характеристики збережено:", stats_file)

