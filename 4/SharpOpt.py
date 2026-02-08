# Алгоритм оптимізації портфеля за Шарпом (Maximum Sharpe Ratio)
#Мета: максимізувати коефіцієнт Шарпа, тобто співвідношення доходності до ризику:				S=(R_p-R_f)/σ_p 
#де R_f– безризикова ставка.
#Кроки:
#	Вхідні дані: μ_i, Σ, R_f
#	Генерація можливих портфелів:
#	ваги w_i, які задовольняють ∑w_i=1і w_i≥0
#	Обчислення характеристик:
#	доходність R_p=∑_i▒w_i  μ_i
#	ризик σ_p=√(w^T Σw)
#	Шарп: S=(R_p-R_f)/σ_p
#	Відбір портфелів з потрібним ризиком (опціонально)
#	Вибір портфеля з максимальним Шарпом
#	Результат: оптимальні ваги, доходність, ризик, Sharpe Ratio

import pandas as pd
import numpy as np
# Завантаження матриці доходностей
file_path = r"D:\A1\stocks_daily_returns_matrix.xlsx"
returns = pd.read_excel(file_path, index_col=0)
expected_returns = returns.mean()
cov_matrix = returns.cov()
tickers = returns.columns
n_assets = len(tickers)
n_portfolios = 50000
tolerance = 0.01
rf = 0  # безризикова ставка для простоти
# Початковий коефіцієнт ризику
risk_factor = 1.0
while True:
    risk_target = returns.std().mean() * risk_factor
    results = []
    # Генерація випадкових портфелів
    for _ in range(n_portfolios):
        weights = np.random.random(n_assets)
        weights /= np.sum(weights)
        port_return = np.dot(weights, expected_returns)
        port_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe_ratio = (port_return - rf) / port_volatility
        if abs(port_volatility - risk_target) < tolerance:
            results.append((weights, port_return, port_volatility, sharpe_ratio))
    # Перевірка
    if results:
        best_portfolio = max(results, key=lambda x: x[3])  # максимальний Sharpe
        best_weights, best_return, best_volatility, best_sharpe = best_portfolio
        portfolio_df = pd.DataFrame({
            "Ticker": tickers,
            "Weight": best_weights
        })
        portfolio_df["Expected_Return"] = best_return
        portfolio_df["Volatility"] = best_volatility
        portfolio_df["Sharpe_Ratio"] = best_sharpe
        output_file = r"D:\A1\optimal_portfolio_sharpe.xlsx"
        portfolio_df.to_excel(output_file, index=False)
        print("Оптимальний портфель за Шарпом збережено:", output_file)
        break
    else:
        print(f"Не знайдено портфеля з ризиком, рівним {risk_target:.6f}.")
        risk_factor = float(input("Введіть коефіцієнт збільшення ризику (наприклад, 1.5): "))
