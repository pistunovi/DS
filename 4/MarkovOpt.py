# Алгоритм оптимізації портфеля за Марковіцем (Mean-Variance)
#Мета: максимізувати очікувану доходність портфеля при заданому рівні ризику (σ).
#	Вхідні дані:
#	середні доходності акцій μ_i
#	коваріаційна матриця Σ
#	Випадкове або чисельне формування портфелів:
#	генеруємо набори ваг w_i, що задовольняють ∑w_i=1і w_i≥0
#	Обчислення характеристик портфеля:
#	доходність: R_p=∑_i▒w_i  μ_i
#	ризик: σ_p=√(w^T Σw)
#	Відбір портфелів з потрібним ризиком (у нашому випадку ± tolerance)
#	Вибір портфеля з максимальною доходністю
#	Результат: оптимальні ваги, доходність і ризик портфеля
#В класичному підході Марковіца можна також розв’язувати аналітично через квадратичне програмування, але ми робили чисельний пошук через SLSQP або перебір.

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
tolerance = 0.01  # ±1% від цільового ризику
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
        if abs(port_volatility - risk_target) < tolerance:
            results.append((weights, port_return, port_volatility))
    # Перевірка
    if results:
        best_portfolio = max(results, key=lambda x: x[1])
        best_weights, best_return, best_volatility = best_portfolio
        portfolio_df = pd.DataFrame({
            "Ticker": tickers,
            "Weight": best_weights
        })
        portfolio_df["Expected_Return"] = best_return
        portfolio_df["Volatility"] = best_volatility

        output_file = r"D:\A1\optimal_portfolio_markowitz.xlsx"
        portfolio_df.to_excel(output_file, index=False)
        print("Оптимальний портфель за Марковіцем збережено:", output_file)
        break
    else:
        print(f"Не знайдено портфеля з ризиком, рівним {risk_target:.6f}.")
        # запит на введення нового коефіцієнта
        risk_factor = float(input("Введіть коефіцієнт збільшення ризику (наприклад, 1.5): "))
