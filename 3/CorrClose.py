#Знайдемо матрицю кореляцій акцій (Close). 
# Тут ми аналізуємо як змінюються ціни закриття акцій відносно одна одної.
import pandas as pd
# Завантаження очищених даних
file_path = r"D:\A1\stocks_parsing_part1_with_returns_cleaned.xlsx"
df = pd.read_excel(file_path)
# Переконуємося, що Date — datetime
df["Date"] = pd.to_datetime(df["Date"])
#  Формуємо таблицю: дати × акції
close_wide = df.pivot(index="Date", columns="Ticker", values="Close")
# Кореляційна матриця
corr_matrix = close_wide.corr()
#  Збереження у Excel
corr_file = r"D:\A1\stocks_correlation_close.xlsx"
corr_matrix.to_excel(corr_file)
print("Матриця кореляцій цін закриття збережена:", corr_file)
