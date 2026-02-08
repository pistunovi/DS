# код для виконання тієї ж задачі через офіційний API Yahoo Finance (RapidAPI).
import requests
import pandas as pd
from datetime import datetime, date
# 1. Список компаній та тикерів
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
# 2. Період збору даних
start_date = int(datetime(2023, 1, 1).timestamp())
end_date = int(datetime.today().timestamp())

# 3. Параметри API (Yahoo Finance через RapidAPI)
url_template = "https://yahoo-finance15.p.rapidapi.com/api/yahoo/historical/{ticker}/USD/1d"
headers = {
    "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",  # <- сюди встав свій ключ
    "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com"
}
all_data = []
for name, ticker in tickers.items():
    url = url_template.format(ticker=ticker)
    response = requests.get(url, headers=headers)
 if response.status_code != 200:
        print(f"Помилка для {ticker}: {response.status_code}")
        continue   
    data = response.json()["items"]  # список щоденних спостережень    
    # Перетворення у DataFrame
    df = pd.DataFrame(data)    
    # Дата у datetime
    df["Date"] = pd.to_datetime(df["date"])    
    # Фільтруємо по датах
    df = df[(df["Date"] >= pd.Timestamp("2023-01-01")) & (df["Date"] <= pd.Timestamp(date.today()))]    
    # Додаємо стовпці Company та Ticker
    df["Company"] = name
    df["Ticker"] = ticker    
    # Денна дохідність
    df = df.sort_values("Date")  # обов'язково сортуємо перед pct_change
    df["Daily_Return"] = df["close"].pct_change()    
    # Вибір стовпців
    df = df[["Company", "Ticker", "Date", "open", "high", "low", "close", "volume", "Daily_Return"]]    
    all_data.append(df)
# Об'єднання всіх компаній
final_df = pd.concat(all_data, ignore_index=True)
final_df = final_df.sort_values(by=["Company", "Date"])
# Збереження в Excel
file_path = r"D:\A1\stocks_api_part1.xlsx"
final_df.to_excel(file_path, index=False)
print("Файл з історичними цінами та денними дохідностями через API збережено:", file_path)
