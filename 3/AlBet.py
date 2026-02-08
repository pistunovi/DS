# озрахуємо Коефіцієнти α (альфа) та β (бета) за моделлю CAPM. 
# Ми розрахуємо альфа і бета для кожної акції відносно індексу ринку 
# (для прикладу можна взяти S&P500, тикер ^GSPC).
import pandas as pd
import yfinance as yf
import statsmodels.api as sm
# Завантаження очищених даних
file_path = r"D:\A1\stocks_parsing_part1_with_returns_cleaned.xlsx"
df = pd.read_excel(file_path)
#  Date → datetime (timezone-naive)
df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None)
#  Завантаження ринкового індексу (S&P 500)
sp500 = yf.Ticker("^GSPC").history(
    start="2023-01-01",
    end=pd.Timestamp.today()
)
#  РОЗВ’ЯЗАННЯ ПРОБЛЕМИ TZ
sp500.index = sp500.index.tz_localize(None)
#  Денна дохідність ринку
sp500["Daily_Return"] = sp500["Close"].pct_change()
market_returns = sp500["Daily_Return"]
alphas = []
betas = []
tickers = df["Ticker"].unique()
#  CAPM-регресія
for ticker in tickers:
    stock_returns = (
        df[df["Ticker"] == ticker][["Date", "Daily_Return"]]
        .set_index("Date")
    )
    combined = (
        stock_returns
        .join(market_returns.rename("Market_Return"), how="inner")
        .dropna()
    )
    # r_i = α + β r_m
    X = sm.add_constant(combined["Market_Return"])
    y = combined["Daily_Return"]
    model = sm.OLS(y, X).fit()
    alphas.append(model.params["const"])
    betas.append(model.params["Market_Return"])
#  Результат
capm_df = pd.DataFrame({
    "Ticker": tickers,
    "Alpha": alphas,
    "Beta": betas
})
#  Збереження
capm_file = r"D:\A1\stocks_alpha_beta.xlsx"
capm_df.to_excel(capm_file, index=False)
print("Таблиця Alpha/Beta збережена:", capm_file)
