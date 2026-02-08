# Тепер визначимо матрицю коваріації денних дохідності. 
# Тут аналізуємо ризик (варіативність) та взаємозв’язок денних дохідності.
import pandas as pd
# Завантаження очищених даних
file_path = r"D:\A1\stocks_parsing_part1_with_returns_cleaned.xlsx"
df = pd.read_excel(file_path)
# Перетворення дати у datetime
df["Date"] = pd.to_datetime(df["Date"])
# Формування таблиці: дати × тикери (денна дохідність)
returns_wide = df.pivot(index="Date", columns="Ticker", values="Daily_Return")
# Видалення пропусків (обов’язково для коректної коваріації)
returns_wide = returns_wide.dropna()
#  Коваріаційна матриця
cov_matrix = returns_wide.cov()
# Збереження у Excel
cov_file = r"D:\A1\stocks_covariance_returns.xlsx"
cov_matrix.to_excel(cov_file)
print("Матриця коваріацій денних дохідностей збережена:", cov_file)
