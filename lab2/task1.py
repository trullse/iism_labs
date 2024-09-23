import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def generate_random_variable_exponential(n):
    u = np.random.uniform(0, 1, n)
    # exponential distribution (y = λe^-λx): λ = 1
    return -np.log(1 - u)


def simulate():
    n = int(entry_n.get())

    data = generate_random_variable_exponential(n)

    mean_estimate = np.mean(data)
    var_estimate = np.var(data)

    confidence_level = 0.95
    ci = stats.t.interval(confidence_level, len(data) - 1, loc=mean_estimate, scale=stats.sem(data))

    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, f"Точечная оценка среднего: {mean_estimate:.4f}\n")
    text_output.insert(tk.END, f"Точечная оценка дисперсии: {var_estimate:.4f}\n")
    text_output.insert(tk.END, f"Доверительный интервал для среднего (95%): {ci}\n")

    plt.figure()
    count, bins, ignored = plt.hist(data, bins=30, density=True, edgecolor='black', alpha=0.7)

    x = np.linspace(min(data), max(data), 1000)
    plt.plot(x, stats.expon.pdf(x), 'r-', lw=2, label='Теоретическая плотность')

    plt.title(f'Гистограмма экспоненциального распределения и теоретическая плотность')
    plt.xlabel('Значение')
    plt.ylabel('Частота')
    plt.legend()
    plt.show()


# GUI setup
root = tk.Tk()
root.title("Симуляция непрерывных случайных величин")

tk.Label(root, text="Введите количество точек выборки:").pack()
entry_n = tk.Entry(root)
entry_n.pack()
entry_n.insert(0, "1000")

tk.Button(root, text="Симулировать", command=simulate).pack()

text_output = tk.Text(root, height=10, width=50)
text_output.pack()

root.mainloop()
