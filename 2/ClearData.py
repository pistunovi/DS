# Завершенням операцій цього типу є очистка даних, що включає в себе:
#1.	Перевірити пропуски (NaN) у всіх стовпцях.
#2.	Видалити або замінити пропуски в Close та Daily_Return.
#3.	Переконатися, що ціни та обсяги ≥ 0.
#4.	Стовпець Date — datetime без часової зони.
#5.	Залишити лише стовпці: Company, Ticker, Date, Open, High, Low, Close, Volume, Daily_Return.
#6.	Зберегти очищену таблицю в окремий файл (наприклад, з суфіксом _cleaned).

import pandas as pd
from pandas.api.types import is_datetime64tz_dtype
# 1. Завантажуємо файл
file_path = r"D:\A1\stocks_parsing_part1_with_returns.xlsx"
df = pd.read_excel(file_path)
# 2. Перевірка типу Date і видалення часової зони
if is_datetime64tz_dtype(df['Date'].dtype):
    df['Date'] = df['Date'].dt.tz_localize(None)
# 3. Видалення рядків з пропусками у критичних стовпцях
df = df.dropna(subset=["Close", "Daily_Return"])
# 4. Замінюємо можливі пропуски у інших стовпцях на останнє відоме значення
df["Volume"] = df["Volume"].fillna(0)
df["Open"] = df["Open"].ffill()
df["High"] = df["High"].ffill()
df["Low"] = df["Low"].ffill()
# 5. Видаляємо некоректні значення (ціни та обсяги < 0)
df = df[(df["Open"] >= 0) & (df["High"] >= 0) & (df["Low"] >= 0) &
        (df["Close"] >= 0) & (df["Volume"] >= 0)]
# 6. Перевірка стовпців і порядок
df = df[["Company", "Ticker", "Date", "Open", "High", "Low", "Close", "Volume", "Daily_Return"]]
# 7. Сортування блоками
df = df.sort_values(by=["Company", "Date"])
# 8. Збереження очищеної таблиці у новий файл
clean_file_path = r"D:\A1\stocks_parsing_part1_with_returns_cleaned.xlsx"
df.to_excel(clean_file_path, index=False)
print("Очищена таблиця збережена у файл:", clean_file_path)
