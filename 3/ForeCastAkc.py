# робимо прогнозування на 3 кроки уперед (3 дні) для кожної акції на основі 
# оригінальної таблиці денних цін закриття.
# Ми використаємо просту модель ARIMA, яка добре підходить 
# для короткострокових прогнозів фінансових часових рядів.
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings("ignore")
# Завантаження оригінальної таблиці
file_path = r"D:\A1\stocks_parsing_part1_with_returns_cleaned.xlsx"
df = pd.read_excel(file_path)
# Підготовка для прогнозу
forecast_horizon = 3  # кількість днів уперед
results = []
tickers = df['Ticker'].unique()
for ticker in tickers:
    stock_data = df[df['Ticker']==ticker].sort_values("Date")
    
    # Використовуємо лише стовпець Close для прогнозу
    ts = stock_data.set_index('Date')['Close']
    
    # Якщо мало даних, пропускаємо
    if len(ts) < 10:
        continue    
    # Простий ARIMA(1,1,1) — можна підібрати оптимальні параметри
    model = ARIMA(ts, order=(1,1,1))
    model_fit = model.fit()    
    # Прогноз на 3 дні уперед
    forecast = model_fit.forecast(steps=forecast_horizon)    
    # Дати прогнозу
    last_date = ts.index[-1]
    forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_horizon)    
    # Додаємо результати
    for date_val, price in zip(forecast_dates, forecast):
        results.append({
            "Ticker": ticker,
            "Company": stock_data['Company'].iloc[0],
            "Forecast_Date": date_val,
            "Forecast_Close": price
        })
# Таблиця прогнозів
forecast_df = pd.DataFrame(results)
# Збереження у Excel
forecast_file = r"D:\A1\stocks_forecast_3days.xlsx"
forecast_df.to_excel(forecast_file, index=False)
print("Прогноз на 3 дні збережено:", forecast_file)
