# автономний скрипт, який:
#•	бере очищений файл
#•	залишає тільки денну дохідність
#•	формує таблицю виду Дата | Amazon | Boeing | Chevron | …
#•	зберігає результат у новий Excel-файл.

import pandas as pd
# Завантаження очищених даних
input_file = r"D:\A1\stocks_parsing_part1_with_returns_cleaned.xlsx"
df = pd.read_excel(input_file)
#  Формат дати
df["Date"] = pd.to_datetime(df["Date"])
#  Формування матриці дохідностей
# Рядки — дати, колонки — компанії
returns_matrix = df.pivot(
    index="Date",
    columns="Company",   # ← якщо хочеш тикери, заміни на "Ticker"
    values="Daily_Return"
)
#  Сортування за датою
returns_matrix = returns_matrix.sort_index()
#  Збереження у новий Excel-файл
output_file = r"D:\A1\stocks_daily_returns_matrix.xlsx"
returns_matrix.to_excel(output_file)
print("Файл з матрицею денних дохідностей створено:")
print(output_file)
