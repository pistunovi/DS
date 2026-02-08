# Перша дія – парсинг даних на свій комп’ютер через можливості Python 
# #з 1.01.2023 по 2.02.2026 за розрахунком дохідності (різниці між поточним
#  закриттям торгів та попередньою датою)
import yfinance as yf
import pandas as pd
from datetime import date
# Список компаній та їх тикери на Yahoo Finance
tickers = {
    "Boeing": "BA",
    "Chevron": "CVX",
    "Caterpillar": "CAT",
    "Microsoft": "MSFT",
    "Walt Disney": "DIS",
    "Coca-Cola": "KO",
    "McDonald’s": "MCD",
    "Amazon.com": "AMZN",
    "NVIDIA": "NVDA",
    "Walmart": "WMT",
    "IBM": "IBM",
    "Nike": "NKE"
}
# Період збору даних
start_date = "2023-01-01"
end_date = date.today().strftime("%Y-%m-%d")  # сьогодні
all_data = []
for name, ticker in tickers.items():
    df = yf.Ticker(ticker).history(start=start_date, end=end_date)
    df.reset_index(inplace=True)
     # Робимо datetime timezone-naive
    df["Date"] = df["Date"].dt.tz_localize(None)
    # Додаємо назву компанії і тикер
    df["Company"] = name
    df["Ticker"] = ticker
    # Денна дохідність
    df["Daily_Return"] = df["Close"].pct_change()
    all_data.append(df)
# Об'єднуємо всі компанії
final_df = pd.concat(all_data, ignore_index=True)
# Сортування блоками
final_df = final_df.sort_values(by=["Company", "Date"])
# Вибір стовпців
final_df = final_df[[
    "Company", "Ticker", "Date", "Open", "High", "Low", "Close", "Volume", "Daily_Return"
]]
# Збереження у Excel
file_path = r"D:\A1\stocks_parsing_part1_with_returns.xlsx"
final_df.to_excel(file_path, index=False)
print("Файл з історичними цінами та денними дохідностями збережено:", file_path)
