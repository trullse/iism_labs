import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
import random
from scipy import stats

values = [1, 2, 3, 4, 5]
probabilities = [0.1, 0.2, 0.3, 0.25, 0.15]


def generate_discrete_random_value(values, probabilities):
    x = random.uniform(0, 1)
    cumulative_probability = 0
    for value, prob in zip(values, probabilities):
        cumulative_probability += prob
        if x < cumulative_probability:
            return value
    return values[-1]


def simulate_discrete_distribution(num_samples):
    samples = [generate_discrete_random_value(values, probabilities) for _ in range(num_samples)]
    return samples


def calculate_confidence_interval(data, confidence=0.95):
    mean = np.mean(data)
    n = len(data)
    se = stats.sem(data)
    interval = se * stats.t.ppf((1 + confidence) / 2., n - 1)
    return mean - interval, mean + interval


def plot_histogram(samples):
    plt.figure(figsize=(8, 6))

    plt.hist(samples, bins=np.arange(min(values) - 0.5, max(values) + 1.5, 1), density=True, alpha=0.7,
             label='Эмпирическое распределение')

    plt.bar(values, probabilities, alpha=0.5, color='red', label='Теоретическое распределение')

    plt.title("Гистограмма выборки")
    plt.xlabel("Значение случайной величины")
    plt.ylabel("Частота")
    plt.legend()
    plt.grid(True)
    plt.show()


def update_text_output(mean_value, conf_interval):
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, f"Точечная оценка среднего: {mean_value:.4f}\n")
    text_output.insert(tk.END, f"Доверительный интервал (95%): ({conf_interval[0]:.4f}, {conf_interval[1]:.4f})\n")


def run_simulation():
    try:
        num_samples = int(entry_num_samples.get())
        if num_samples <= 0:
            raise ValueError

        samples = simulate_discrete_distribution(num_samples)

        mean_value = np.mean(samples)
        conf_interval = calculate_confidence_interval(samples)

        update_text_output(mean_value, conf_interval)

        root.after(100, plot_histogram, samples)

    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректное количество симуляций (целое число > 0)")


root = tk.Tk()
root.title("Имитация дискретных случайных величин")

tk.Label(root, text="Введите количество симуляций:").pack()
entry_num_samples = tk.Entry(root)
entry_num_samples.pack()

tk.Button(root, text="Запустить симуляцию", command=run_simulation).pack()

text_output = tk.Text(root, height=10, width=50)
text_output.pack()

root.mainloop()
