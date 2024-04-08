import tkinter as tk
from tkinter import messagebox
import random
import numpy as np

# Defining game configurations such as number of rows and columns, colors and font...
num_rows = 3
num_columns = 6
card_size_w = 20
card_size_h = 10
color_back = "#343a40"
color_letters = "#c6c7c8"
color_card = "#000000"
font_style = ('Arial', 12, 'bold')
max_try = 18

# Defining word pairs (German: English)

word_pairs = {
    "Haus": "House",
    "Auto": "Car",
    "Apfel": "Apple",
    "Katze": "Cat",
    "Hund": "Dog",
    "Zucker": "Sugar",
    "Milch": "Milk",
    "Flasche": "Bottle",
    "Regal": "Shelf",
    # Add more word pairs as needed
}

# Creating grid with the words, two lists from the dictionary. One with the german words and another list with the English words.
def create_card_grid():
    word_list_german = list(word_pairs.keys())
    word_list_english = list(word_pairs.values())
    random.shuffle(word_list_english)
    random.shuffle(word_list_german)
    combined_words = list(zip(word_list_english, word_list_german))
    grid_flat = np.array(combined_words[:num_rows * num_columns])
    grid = grid_flat.reshape((num_rows, num_columns))
    return grid

grid = create_card_grid()
cards = []
card_revealed = []
card_correspond = []
num_attempts = 0


# Creating function clicking cards
def card_clicked(rows, columns):
    card = cards[rows][columns]
    if card['text'] == '':
        word = grid[rows][columns]
        card.config(text=word, fg=color_letters)
        card_revealed.append(card)
        if len(card_revealed) == 2:
            check_match()


# Check if two revealed cards match. It is a macth if the word in german matchs its tranlation in English
def check_match():
    global card1, card2
    
    card1, card2 = card_revealed

    for german, english in word_pairs.items():
        if card1['text'] == f"{german}" and card2['text'] == f"{english}":
            card1.after(1000, card1.destroy)
            card2.after(1000, card2.destroy)
            card_correspond.extend([card1, card2])
            check_win()
        elif card1['text'] == f"{english}" and card2["text"] == f"{german}":
            card1.after(1000, card1.destroy)
            card2.after(1000, card2.destroy)
            card_correspond.extend([card1, card2])
            check_win()
    else:
        card1.after(1000, lambda: card1.config(text='', fg='black'))
        card2.after(1000, lambda: card2.config(text='', fg='black'))
    
    card_revealed.clear()
    update_score()


# Checking if all pairs have been matched
def check_win():
    if len(card_correspond) == num_rows * num_columns:
        messagebox.showinfo("Wunderbar!", "You've matched all pairs!")
        windows.quit()

# Updating score and checking if the player lost
def update_score():
    global num_attempts
    num_attempts += 1
    label_attempts.config(text='Attempts: {}/{}'.format(num_attempts, max_try))
    if num_attempts >= max_try:
        messagebox.showinfo("Spiel vorbei", "You've reached the maximum number of attempts!")
        windows.quit()

# Creating the game interface
windows = tk.Tk()
windows.title('Memory Game Word German English')
windows.configure(bg=color_back)

# Personalizing button style
button_style = {'activebackground': '#f8f9fa', 'font': font_style, 'fg': color_letters}
windows.option_add('*Button', button_style)

# Label for number of attempts
label_attempts = tk.Label(windows, text='Attempts: {}/{}'.format(num_attempts, max_try), fg=color_letters, bg=color_back, font=font_style)
label_attempts.grid(row=num_rows, columnspan=num_columns, padx=10, pady=10)

# Creating grid of cards with word pairs
for rows in range(num_rows):
    row_cards = []
    for col in range(num_columns):
        card = tk.Button(windows, command=lambda r=rows, c=col: card_clicked(r, c), width=card_size_w, height=card_size_h, bg=color_card, fg=color_card, relief=tk.RAISED, bd=3)
        card.grid(row=rows, column=col, padx=5, pady=5)
        row_cards.append(card)
    cards.append(row_cards)

windows.mainloop()

