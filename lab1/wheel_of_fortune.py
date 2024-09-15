import tkinter as tk
from tkinter import messagebox, Canvas
import random
import math

donation_data = {}
game_colors = {}


def add_donation(game, amount):
    if game in donation_data:
        donation_data[game] += amount
    else:
        donation_data[game] = amount
        game_colors[game] = f'#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}'


def calculate_probabilities():
    total_donations = sum(donation_data.values())
    if total_donations == 0:
        return None
    probabilities = {game: amount / total_donations for game, amount in donation_data.items()}
    return probabilities


def calculate_stop_angle(selected_game):
    if not donation_data:
        return 0

    total_prob = 0
    for game in donation_data.keys():
        probability = calculate_probabilities()[game]
        start_angle = total_prob * 360
        total_prob += probability
        end_angle = total_prob * 360

        if game == selected_game:
            random_angle = random.uniform(start_angle, end_angle)
            return random_angle

    return 0


def simulate_wheel():
    probabilities = calculate_probabilities()
    if not probabilities:
        return None

    rand_val = random.random()
    cumulative_prob = 0

    for game in donation_data.keys():
        prob = probabilities[game]
        cumulative_prob += prob
        if rand_val < cumulative_prob:
            return game

    return None


def add_donation_entry():
    try:
        game = game_entry.get()
        amount = float(amount_entry.get())
        if game == "" or amount <= 0:
            raise ValueError
        add_donation(game, amount)
        update_game_list()
        game_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid game and a positive donation amount.")


def update_game_list():
    game_list.delete(0, tk.END)
    for game, amount in donation_data.items():
        game_list.insert(tk.END, f"{game}: ${amount:.2f}")
    draw_wheel()


def draw_wheel(start_angle=0):
    canvas.delete("all")
    if not donation_data:
        return
    probabilities = calculate_probabilities()
    current_angle = start_angle

    for game in donation_data.keys():
        probability = probabilities[game]
        extent = probability * 360
        color = game_colors[game]

        canvas.create_arc(50, 50, 350, 350, start=current_angle, extent=extent, fill=color, outline="black")

        mid_angle = current_angle + extent / 2
        label_x = 200 + 150 * math.cos(math.radians(mid_angle))
        label_y = 200 - 150 * math.sin(math.radians(mid_angle))

        canvas.create_text(label_x, label_y, text=game, fill="black")

        current_angle += extent

    canvas.create_polygon(195, 30, 205, 30, 200, 50, fill='red')


def spin_wheel():
    probabilities = calculate_probabilities()
    if not probabilities:
        messagebox.showwarning("Error", "No games to spin for!")
        return

    selected_game = simulate_wheel()
    stop_angle = calculate_stop_angle(selected_game)

    # Simulate spinning
    spins = random.randint(1, 3) * 360
    total_angle = spins + 360 - stop_angle + 90

    steps = 100
    current_angle = 0
    slowdown_factor = 1.02

    for step in range(steps):
        current_angle += (total_angle / steps)
        draw_wheel(current_angle % 360)
        canvas.after(int(10 * slowdown_factor))
        slowdown_factor *= 1.02
        canvas.update()

    draw_wheel(total_angle % 360)
    messagebox.showinfo("Result", f"The wheel choice: {selected_game}")


root = tk.Tk()
root.title("Wheel of Fortune")

tk.Label(root, text="Game:").pack()
game_entry = tk.Entry(root)
game_entry.pack()

tk.Label(root, text="Donation Amount:").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Button(root, text="Add Donation", command=add_donation_entry).pack()

tk.Label(root, text="Current Donations:").pack()
game_list = tk.Listbox(root, width=40, height=10)
game_list.pack()

canvas = Canvas(root, width=400, height=400)
canvas.pack()

tk.Button(root, text="Spin the Wheel", command=spin_wheel).pack()

root.mainloop()
