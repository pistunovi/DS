# Попередні задачі вирішувалися повним перебором із 50000 варіантів, але при необхідності можна вирішити нелінійну оптимізаційну задачу:
#•	Цільова функція із логарифмом ризику
#•	Обмеження: сума ваг = 1 та квадрат ризику ≤ заданий поріг 
# Тобто цільова функція нелінійна через логарифм, а обмеження квадратичне.
# На тих же даних що і попередні

import pandas as pd
import numpy as np
from scipy.optimize import minimize
# Завантаження матриці доходностей
file_path = r"D:\A1\stocks_daily_returns_matrix.xlsx"
returns = pd.read_excel(file_path, index_col=0)
expected_returns = returns.mean().values
cov_matrix = returns.cov().values
n_assets = len(expected_returns)
#  Параметр штрафу
lambda_penalty = 1.0
#  Поріг ризику (квадратна функція)
risk_limit = (returns.std().mean() * 3)**2
# 4️⃣ Цільова функція (максимізація логарифмічного штрафу ризику)
def objective(weights):
    port_return = np.dot(weights, expected_returns)
    port_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
    return -(port_return - lambda_penalty * np.log(1 + port_variance))
#  Обмеження
constraints = [
    {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},                # сума ваг = 1
    {'type': 'ineq', 'fun': lambda w: risk_limit - np.dot(w.T, np.dot(cov_matrix, w))**2}  # квадрат ризику ≤ risk_limit
]
#  Межі для ваг
bounds = tuple((0, 1) for _ in range(n_assets))
#  Початкове наближення
x0 = np.ones(n_assets) / n_assets
#  Оптимізація
result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
if result.success:
    optimal_weights = result.x
    port_return = np.dot(optimal_weights, expected_returns)
    port_variance = np.dot(optimal_weights.T, np.dot(cov_matrix, optimal_weights))
    portfolio_df = pd.DataFrame({
        'Ticker': returns.columns,
        'Weight': optimal_weights
    })
    portfolio_df['Expected_Return'] = port_return
    portfolio_df['Portfolio_Variance'] = port_variance
    output_file = r"D:\A1\nonlinear_log_square_portfolio.xlsx"
    portfolio_df.to_excel(output_file, index=False)
    print("Оптимальний нелінійний портфель з логарифмом та квадратом обмеження збережено:", output_file)
else:
    print("Оптимізація не вдалася:", result.message)
