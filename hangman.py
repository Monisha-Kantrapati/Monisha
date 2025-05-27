import tkinter as tk
import random
from tkinter import messagebox, ttk

# ------------------ Word List ------------------ #
WORDS = [
    "python", "hangman", "challenge", "programming", "openai", "interface", "keyboard", "developer",
    "algorithm", "function", "variable", "condition", "iteration", "exception", "syntax", "parameter",
    "compile", "debugging", "repository", "software", "hardware", "database", "encryption", "firewall",
    "network", "protocol", "server", "client", "packet", "bandwidth", "latency", "cache",
    "thread", "process", "memory", "storage", "virtualization", "container", "docker", "kubernetes",
    "cloud", "automation", "script", "binary", "operator", "expression", "inheritance", "polymorphism",
    "encapsulation", "abstraction", "constructor", "destructor", "interface", "module", "package",
    "library", "framework", "frontend", "backend", "fullstack", "debugger", "compiler", "interpreter",
    "syntax", "semantics", "runtime", "exception", "interface", "object", "class", "method", "attribute",
    "array", "list", "dictionary", "tuple", "set", "queue", "stack", "graph", "tree", "binarysearch",
    "sorting", "searching", "recursion", "iteration", "complexity", "algorithm", "database", "query",
    "index", "transaction", "commit", "rollback", "authentication", "authorization"
]

# ------------------ Main Game Class ------------------ #
class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Hangman Game")
        self.root.geometry("600x500")
        self.root.config(bg="#FDEBD0")

        # Game stats
        self.wins = 0
        self.losses = 0

        # Difficulty settings
        self.difficulty_settings = {"Easy": 8, "Medium": 6, "Hard": 4}
        self.current_difficulty = "Medium"  # Default difficulty
        self.word = random.choice(WORDS)
        self.display_word = ['_' for _ in self.word]
        self.guessed_letters = set()
        self.incorrect_guesses = set()
        self.remaining_guesses = self.difficulty_settings[self.current_difficulty]

        self.create_widgets()

    def create_widgets(self):
        # Title
        self.title = tk.Label(self.root, text="🎮 Hangman Game", font=("Arial", 24, "bold"), bg="#FDEBD0", fg="#5D6D7E")
        self.title.pack(pady=10)

        # Wins and Losses
        self.stats_label = tk.Label(self.root, text=f"Wins: {self.wins} | Losses: {self.losses}", font=("Arial", 14), bg="#FDEBD0", fg="#2E4053")
        self.stats_label.pack(pady=5)

        # Difficulty selection
        self.difficulty_label = tk.Label(self.root, text="Select Difficulty:", font=("Arial", 12), bg="#FDEBD0")
        self.difficulty_label.pack()
        self.difficulty_var = tk.StringVar(value=self.current_difficulty)
        self.difficulty_menu = ttk.Combobox(self.root, textvariable=self.difficulty_var, values=list(self.difficulty_settings.keys()), state="readonly")
        self.difficulty_menu.pack(pady=5)
        self.difficulty_menu.bind("<<ComboboxSelected>>", self.change_difficulty)

        # Word display
        self.word_label = tk.Label(self.root, text=' '.join(self.display_word), font=("Courier", 28), bg="#FDEBD0")
        self.word_label.pack(pady=20)

        # Guess entry and button
        self.guess_entry = tk.Entry(self.root, font=("Arial", 16), justify="center")
        self.guess_entry.pack()
        self.guess_button = tk.Button(self.root, text="Guess", font=("Arial", 14), bg="#AED6F1", command=self.make_guess)
        self.guess_button.pack(pady=5)

        # Hint button
        self.hint_button = tk.Button(self.root, text="Hint (-1 Guess)", font=("Arial", 12), bg="#F9E79F", command=self.give_hint)
        self.hint_button.pack(pady=5)

        # Info label (remaining guesses)
        self.info_label = tk.Label(self.root, text=f"Remaining Guesses: {self.remaining_guesses}", font=("Arial", 14), bg="#FDEBD0", fg="red")
        self.info_label.pack(pady=5)

        # Incorrect guesses display
        self.incorrect_label = tk.Label(self.root, text="Incorrect Guesses: None", font=("Arial", 12), bg="#FDEBD0", fg="#C0392B")
        self.incorrect_label.pack(pady=5)

        # Reset button
        self.reset_button = tk.Button(self.root, text="Reset Game", font=("Arial", 12), bg="#D7BDE2", command=self.reset_game)
        self.reset_button.pack(pady=5)

    def change_difficulty(self, event):
        self.current_difficulty = self.difficulty_var.get()
        self.remaining_guesses = self.difficulty_settings[self.current_difficulty]
        self.info_label.config(text=f"Remaining Guesses: {self.remaining_guesses}")
        self.reset_game()

    def give_hint(self):
        if self.remaining_guesses <= 1:
            messagebox.showwarning("No Guesses Left", "You need at least 1 guess to use a hint!")
            return

        # Find unguessed letters in the word
        unguessed = [letter for letter in self.word if letter not in self.guessed_letters]
        if not unguessed:
            return

        # Reveal a random unguessed letter
        hint_letter = random.choice(unguessed)
        self.guessed_letters.add(hint_letter)
        for idx, letter in enumerate(self.word):
            if letter == hint_letter:
                self.display_word[idx] = hint_letter
        self.word_label.config(text=' '.join(self.display_word))
        
        # Deduct a guess
        self.remaining_guesses -= 1
        self.info_label.config(text=f"Remaining Guesses: {self.remaining_guesses}")
        self.check_game_over()

    def make_guess(self):
        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, tk.END)

        if not guess.isalpha() or len(guess) != 1:
            messagebox.showwarning("Invalid Input", "Please enter a single letter.")
            return

        if guess in self.guessed_letters:
            messagebox.showinfo("Oops!", f"You already guessed '{guess}'.")
            return

        self.guessed_letters.add(guess)

        if guess in self.word:
            for idx, letter in enumerate(self.word):
                if letter == guess:
                    self.display_word[idx] = guess
            self.word_label.config(text=' '.join(self.display_word))
        else:
            self.remaining_guesses -= 1
            self.incorrect_guesses.add(guess)
            self.incorrect_label.config(text=f"Incorrect Guesses: {', '.join(sorted(self.incorrect_guesses)) if self.incorrect_guesses else 'None'}")

        self.info_label.config(text=f"Remaining Guesses: {self.remaining_guesses}")
        self.check_game_over()

    def check_game_over(self):
        if '_' not in self.display_word:
            self.wins += 1
            messagebox.showinfo("🎉 You Win!", f"Congratulations! You guessed the word: {self.word}")
            self.stats_label.config(text=f"Wins: {self.wins} | Losses: {self.losses}")
            self.disable_input()
        elif self.remaining_guesses == 0:
            self.losses += 1
            messagebox.showinfo("😢 Game Over", f"You ran out of guesses. The word was: {self.word}")
            self.stats_label.config(text=f"Wins: {self.wins} | Losses: {self.losses}")
            self.disable_input()

    def disable_input(self):
        self.guess_entry.config(state='disabled')
        self.guess_button.config(state='disabled')
        self.hint_button.config(state='disabled')

    def reset_game(self):
        self.word = random.choice(WORDS)
        self.display_word = ['_' for _ in self.word]
        self.guessed_letters.clear()
        self.incorrect_guesses.clear()
        self.remaining_guesses = self.difficulty_settings[self.current_difficulty]

        self.word_label.config(text=' '.join(self.display_word))
        self.info_label.config(text=f"Remaining Guesses: {self.remaining_guesses}")
        self.incorrect_label.config(text="Incorrect Guesses: None")
        self.guess_entry.config(state='normal')
        self.guess_button.config(state='normal')
        self.hint_button.config(state='normal')

# ------------------ Start the App ------------------ #
if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
