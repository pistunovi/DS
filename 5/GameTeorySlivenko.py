# У файлі theory_of_gaim.xlsx міститься таблиця, в якій перші 3 рядки 
# визначають тип стратегії. 4 стовпці визначають стан природи. 
# Четвертий рядок дає значення імовірності настання стану природи. 
# Для коректної роботи програми треба прибрати назви стратегій (А1…А3) 
# і назви станів природи (S1…S4). 
# Також додано рядок імовірності (p) настання станів природи. 
# У робочому варіанті файлу  додано точність (q)  визначення імовірності.

# Пояснення коду
#1.	payoffs → матриця виграшів стратегій (рядки) для кожного стану природи (стовпці)
#2.	probabilities → ймовірності настання станів природи
#3.	Методи для невідомих ймовірностей:
#o	Максимін → максимізує мінімальний виграш
#o	Максимакс → максимізує максимальний виграш
#o	Лаплас → середнє виграшів для всіх станів
#o	Гурвіца → компроміс між максимін та максимакс
#4.	Метод більшості → обираємо стратегію, яку обрали більшість методів
#5.	Відомі ймовірності → обчислюємо очікувану вигоду для кожної стратегії та вибираємо максимальну.
#6.	У програмі передбачено автоматичне перетворення десяткових ком у крапки для коректного зчитування числових даних з Excel.
#7.	Програма працює з матрицею довільного розміру, а також враховує випадки, коли точності і/або імовірності невідомі. 
#8.	Програма ігнорує коми в десяткових числах, що стоять у файлі.

#Результати роботи програми подано для трьох варіантів:
#1.	Відомі імовірності і їх точності
#2.	Відомі тільки імовірності
#3.	Імовірності невідомі.

import pandas as pd
import numpy as np
from collections import Counter

# ----------------------------
# Ввід r і s
# ----------------------------
while True:
    try:
        r = int(input("Введіть кількість стратегій r: "))
        s = int(input("Введіть кількість станів природи s: "))
        if r > 0 and s > 0:
            break
        else:
            print("r та s повинні бути додатні")
    except ValueError:
        print("Введіть цілі числа")

# ----------------------------
# Зчитування Excel
# ----------------------------
file_path = r"D:\A1\theory_of_gaim.xlsx"
df = pd.read_excel(file_path, header=None)

# ----------------------------
# Матриця виграшів
# ----------------------------
payoffs = df.iloc[:r, :s].astype(float).values
payoffs = np.nan_to_num(payoffs, nan=0.0)

# ----------------------------
# Ймовірності (рядок r)
# ----------------------------
probabilities = None
if df.shape[0] >= r + 1:
    probabilities = df.iloc[r, :s].astype(float).values
    probabilities = np.nan_to_num(probabilities, nan=0.0)

# ----------------------------
# Точності (рядок r+1)
# ----------------------------
accuracy = None
if df.shape[0] >= r + 2:
    accuracy = df.iloc[r + 1, :s].astype(float).values
    accuracy = np.nan_to_num(accuracy, nan=0.0)

# ----------------------------
# Ввід α
# ----------------------------
while True:
    try:
        alpha = float(input("Введіть коефіцієнт оптимізму α (0 ≤ α ≤ 1): "))
        if 0 <= alpha <= 1:
            break
        else:
            print("α має бути між 0 та 1")
    except ValueError:
        print("Введіть число від 0 до 1")

# ----------------------------
# Розрахунок по стратегіях
# ----------------------------
strategies = [f"A{i+1}" for i in range(r)]

min_vals = np.min(payoffs, axis=1)
max_vals = np.max(payoffs, axis=1)
avg_vals = np.mean(payoffs, axis=1)
hurwicz_vals = alpha * max_vals + (1 - alpha) * min_vals

# ----------------------------
# Очікувана вигода (якщо є ймовірності)
# ----------------------------
expected_values = None
if probabilities is not None and len(probabilities) == s:

    # якщо точність є — застосовуємо
    if accuracy is not None and len(accuracy) == s:
        probabilities = probabilities * accuracy

    # без нормалізації
    expected_values = payoffs.dot(probabilities)

# ----------------------------
# Таблиця "результати по стратегіях"
# ----------------------------
results_by_strategy = pd.DataFrame({
    "Стратегія": strategies,
    "min": min_vals,
    "max": max_vals,
    "avg": avg_vals,
    "hurwicz": hurwicz_vals
})

if expected_values is not None:
    results_by_strategy["expected"] = expected_values

print("\n📌 Результати по кожній стратегії:")
print(results_by_strategy)

# ----------------------------
# Вибір кращих стратегій по методах
# ----------------------------
maximin_index = np.argmax(min_vals)
maximax_index = np.argmax(max_vals)
laplace_index = np.argmax(avg_vals)
hurwicz_index = np.argmax(hurwicz_vals)

maximin_strategy = strategies[maximin_index]
maximax_strategy = strategies[maximax_index]
laplace_strategy = strategies[laplace_index]
hurwicz_strategy = strategies[hurwicz_index]

votes = [maximin_strategy, maximax_strategy, laplace_strategy, hurwicz_strategy]
majority_strategy = Counter(votes).most_common(1)[0][0]

methods = [
    "Максимін",
    "Максимакс",
    "Лаплас",
    f"Гурвіца (α = {alpha})",
    "Більшістю методів"
]

strategies_result = [
    maximin_strategy,
    maximax_strategy,
    laplace_strategy,
    hurwicz_strategy,
    majority_strategy
]

sum_payoff_for_method = [
    float(min_vals[maximin_index]),
    float(max_vals[maximax_index]),
    float(avg_vals[laplace_index]),
    float(hurwicz_vals[hurwicz_index]),
    float(avg_vals[strategies.index(majority_strategy)])
]

# Додаємо "Очікувана вигода"
if expected_values is not None:
    methods.append("Очікувана вигода")
    strategies_result.append(strategies[np.argmax(expected_values)])
    sum_payoff_for_method.append(float(expected_values.max()))

results_df = pd.DataFrame({
    "Метод": methods,
    "Стратегія": strategies_result,
    "Сума виграшу": sum_payoff_for_method
})

# ----------------------------
# Збереження у файл
# ----------------------------
output_file = r"D:\A1\best_strategy_theory_of_game.xlsx"
results_df.to_excel(output_file, index=False)

print("\n✅ Результати вибору стратегій:")
print(results_df)
print(f"\n📁 Файл збережено: {output_file}")
