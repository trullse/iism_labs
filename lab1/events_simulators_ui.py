import tkinter as tk
from tkinter import messagebox
from events_simulators import *


def simple_event_check(count):
    try:
        p = float(simple_prob_input.get())
        if not (0 <= p <= 1):
            raise ValueError("Probability must be between 0 and 1.")
        results = [simulate_simple_event(p) for _ in range(count)]
        frequency_true = sum(results) / len(results)
        messagebox.showinfo("Simple Event", f"Probability: {p}\nFrequency: {frequency_true}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid probability between 0 and 1.")


def complex_event_check(count):
    try:
        probabilities = list(map(float, complex_prob_input.get().split()))
        if any(not (0 <= p <= 1) for p in probabilities):
            raise ValueError("All probabilities must be between 0 and 1.")
        results = [simulate_complex_event(probabilities) for _ in range(count)]
        frequencies = [sum(r[i] for r in results) / len(results) for i in range(len(probabilities))]
        messagebox.showinfo("Complex Event", f"Probabilities: {probabilities}\nFrequencies: {frequencies}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid probabilities between 0 and 1, separated by spaces.")


def dependent_event_check(count):
    try:
        p_A = float(dep_prob_A_input.get())
        p_B_given_A = float(dep_prob_B_given_A_input.get())
        if not (0 <= p_A <= 1) or not (0 <= p_B_given_A <= 1):
            raise ValueError("Probabilities must be between 0 and 1.")

        p_not_A = 1 - p_A
        p_B_not_given_A = 1 - p_B_given_A

        # Theoretical probabilities
        prob_A_and_B = p_A * p_B_given_A
        prob_A_and_not_B = p_A * (1 - p_B_given_A)
        prob_not_A_and_B = p_not_A * p_B_not_given_A
        prob_not_A_and_not_B = p_not_A * (1 - p_B_not_given_A)

        # Practical frequencies
        results = [simulate_dependent_event(p_A, p_B_given_A) for _ in range(count)]
        frequencies = [results.count(i) / len(results) for i in range(4)]

        messagebox.showinfo(
            "Dependent Event",
            f"Theoretical Probabilities:\n"
            f"P(A and B): {prob_A_and_B:.6f}\n"
            f"P(A and not B): {prob_A_and_not_B:.6f}\n"
            f"P(not A and B): {prob_not_A_and_B:.6f}\n"
            f"P(not A and not B): {prob_not_A_and_not_B:.6f}\n\n"
            f"Practical Frequencies:\n"
            f"P(A and B): {frequencies[0]:.6f}\n"
            f"P(A and not B): {frequencies[1]:.6f}\n"
            f"P(not A and B): {frequencies[2]:.6f}\n"
            f"P(not A and not B): {frequencies[3]:.6f}"
        )
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid probabilities between 0 and 1.")


def complete_group_check(count):
    try:
        probabilities = list(map(float, complete_group_prob_input.get().split()))
        if any(not (0 <= p <= 1) for p in probabilities):
            raise ValueError("All probabilities must be between 0 and 1.")
        if sum(probabilities) != 1:
            raise ValueError("The sum of probabilities must be equal to 1.")
        if len(probabilities) < 2:
            raise ValueError("There must be at least two probabilities.")

        results = [simulate_complete_group(probabilities) for _ in range(count)]
        frequencies = [results.count(i) / len(results) for i in range(len(probabilities))]

        # Dynamic output for events
        output = "\n".join([f"P(Event {i}): {frequencies[i]:.6f}" for i in range(len(frequencies))])
        messagebox.showinfo("Complete Group Event", f"Frequencies:\n{output}")

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Event Simulation")

    def add_separator():
        separator = tk.Frame(height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill=tk.X, pady=5)


    # Simple Event
    tk.Label(root, text="Simple Event (Enter probability for True):").pack()
    simple_prob_input = tk.Entry(root)
    simple_prob_input.pack()
    tk.Button(root, text="Run Once", command=lambda: simple_event_check(1)).pack()
    tk.Button(root, text="Run 1,000,000 Times", command=lambda: simple_event_check(10 ** 6)).pack()

    add_separator()

    # Complex Event
    tk.Label(root, text="Complex Event (Enter space-separated probabilities):").pack()
    complex_prob_input = tk.Entry(root)
    complex_prob_input.pack()
    tk.Button(root, text="Run Once", command=lambda: complex_event_check(1)).pack()
    tk.Button(root, text="Run 1,000,000 Times", command=lambda: complex_event_check(10 ** 6)).pack()

    add_separator()

    # Dependent Event
    tk.Label(root, text="Dependent Event (Enter P(A) and P(B|A)):").pack()
    dep_prob_A_input = tk.Entry(root)
    dep_prob_A_input.insert(0, "0.6")  # Default value for P(A)
    dep_prob_A_input.pack()
    dep_prob_B_given_A_input = tk.Entry(root)
    dep_prob_B_given_A_input.insert(0, "0.7")  # Default value for P(B|A)
    dep_prob_B_given_A_input.pack()
    tk.Button(root, text="Run Once", command=lambda: dependent_event_check(1)).pack()
    tk.Button(root, text="Run 1,000,000 Times", command=lambda: dependent_event_check(10 ** 6)).pack()

    add_separator()

    # Complete Group Event
    tk.Label(root, text="Complete Group Event (Enter space-separated probabilities summing to 1):").pack()
    complete_group_prob_input = tk.Entry(root)
    complete_group_prob_input.pack()
    tk.Button(root, text="Run Once", command=lambda: complete_group_check(1)).pack()
    tk.Button(root, text="Run 1,000,000 Times", command=lambda: complete_group_check(10 ** 6)).pack()

    root.mainloop()
