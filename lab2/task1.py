import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


# Функция для генерации случайной величины по методу обратных функций
def generate_random_variable(n, dist_type='uniform'):
    u = np.random.uniform(0, 1, n)  # Генерация равномерных случайных чисел
    if dist_type == 'exponential':
        # Пример: Экспоненциальное распределение с параметром λ = 1
        return -np.log(1 - u)
    elif dist_type == 'normal':
        # Пример: Нормальное распределение с μ = 0 и σ = 1 (используем Box-Muller метод)
        z = np.sqrt(-2 * np.log(u)) * np.cos(2 * np.pi * np.random.uniform(0, 1, n))
        return z
    else:
        # Равномерное распределение
        return u


# Функция для построения гистограммы и расчёта точечных/интервальных оценок
def simulate():
    n = int(entry_n.get())
    dist_type = dist_var.get()

    # Генерация случайной величины
    data = generate_random_variable(n, dist_type)

    # Точечные оценки
    mean_estimate = np.mean(data)
    var_estimate = np.var(data)

    # Интервальные оценки для среднего значения
    confidence_level = 0.95
    ci = stats.t.interval(confidence_level, len(data) - 1, loc=mean_estimate, scale=stats.sem(data))

    # Вывод результатов на экран
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, f"Точечная оценка среднего: {mean_estimate:.4f}\n")
    text_output.insert(tk.END, f"Точечная оценка дисперсии: {var_estimate:.4f}\n")
    text_output.insert(tk.END, f"Доверительный интервал для среднего (95%): {ci}\n")

    # Построение гистограммы
    plt.figure()
    count, bins, ignored = plt.hist(data, bins=30, density=True, edgecolor='black', alpha=0.7)

    # Теоретическая плотность вероятности
    x = np.linspace(min(data), max(data), 1000)
    if dist_type == 'exponential':
        # Экспоненциальное распределение (теоретическая плотность)
        plt.plot(x, stats.expon.pdf(x), 'r-', lw=2, label='Теоретическая плотность')
    elif dist_type == 'normal':
        # Нормальное распределение (теоретическая плотность)
        plt.plot(x, stats.norm.pdf(x), 'r-', lw=2, label='Теоретическая плотность')
    else:
        # Равномерное распределение (теоретическая плотность)
        plt.plot(x, stats.uniform.pdf(x, 0, 1), 'r-', lw=2, label='Теоретическая плотность')

    plt.title(f'Гистограмма {dist_type}-распределения и теоретическая плотность')
    plt.xlabel('Значение')
    plt.ylabel('Частота')
    plt.legend()
    plt.show()


# GUI setup
root = tk.Tk()
root.title("Симуляция непрерывных случайных величин")

# Выбор распределения
tk.Label(root, text="Выберите распределение:").pack()
dist_var = tk.StringVar(value='uniform')
tk.Radiobutton(root, text="Равномерное", variable=dist_var, value='uniform').pack()
tk.Radiobutton(root, text="Экспоненциальное", variable=dist_var, value='exponential').pack()
tk.Radiobutton(root, text="Нормальное", variable=dist_var, value='normal').pack()

# Ввод количества точек
tk.Label(root, text="Введите количество точек выборки:").pack()
entry_n = tk.Entry(root)
entry_n.pack()
entry_n.insert(0, "1000")

# Кнопка для запуска симуляции
tk.Button(root, text="Симулировать", command=simulate).pack()

# Поле для вывода результатов
text_output = tk.Text(root, height=10, width=50)
text_output.pack()

root.mainloop()
