import tkinter as tk
import random

class GuessTheNumberGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Guess the Number")
        self.best_score = None
        self.create_widgets()
        self.start_new_game()

    def create_widgets(self):
        self.intro_text = tk.Label(self.master, text="Welcome to Guess the Number!", font=("Helvetica", 25))
        self.intro_text.grid(row=0, column=0, columnspan=3, padx=20, pady=10)
        # Column 1 widgets
        self.game_mode_text = tk.Label(self.master, text="Guess a number!", font=("Helvetica", 14))
        self.game_mode_text.grid(row=1, column=0, padx=20, pady=10, sticky='w')

        self.feedback_label = tk.Label(self.master, text="", font=("Helvetica", 14))
        self.feedback_label.grid(row=2, column=0, padx=20, pady=10, sticky='w')

        self.attempts_counter = tk.Label(self.master, text="", font=("Helvetica", 14))
        self.attempts_counter.grid(row=3, column=0, padx=20, pady=10, sticky='w')


        self.number_label = tk.Label(self.master, text="Number: ?", font=("Helvetica", 20))
        self.number_label.grid(row=4, column=0, padx=20, pady=10, sticky='w')

        self.entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.entry.grid(row=5, column=0, padx=20, pady=5, sticky='w')

        self.submit_button = tk.Button(self.master, text="Submit", command=self.check_guess, font=("Helvetica", 12), width=15)
        self.submit_button.grid(row=6, column=0, padx=20, pady=20, sticky='w')

        self.start_button = tk.Button(self.master, text="Start Game", command=self.start_new_game, font=("Helvetica", 12), width=15)
        self.start_button.grid(row=7, column=0, padx=20, pady=10, sticky='w')

        self.restart_button = tk.Button(self.master, text="Restart", command=self.start_new_game, font=("Helvetica", 12), width=15)
        self.restart_button.grid(row=8, column=0, padx=20, pady=10, sticky='w')

        # Column 2 widgets
        self.best_score_label = tk.Label(self.master, text="Best Score: No attempts yet", font=("Helvetica", 20))
        self.best_score_label.grid(row=2, column=1, padx=20, pady=10)

        self.difficulty_label = tk.Label(self.master, text="Select difficulty level:", font=("Helvetica", 14))
        self.difficulty_label.grid(row=4, column=1, padx=20, pady=10)

        self.difficulty_var = tk.StringVar(value="Medium")
        tk.Radiobutton(self.master, text="Easy (1-10)", variable=self.difficulty_var, value="Easy", font=("Helvetica", 12)).grid(row=5, column=1, padx=20, pady=5)
        tk.Radiobutton(self.master, text="Medium (1-100)", variable=self.difficulty_var, value="Medium", font=("Helvetica", 12)).grid(row=6, column=1, padx=20, pady=5)
        tk.Radiobutton(self.master, text="Hard (1-1000)", variable=self.difficulty_var, value="Hard", font=("Helvetica", 12)).grid(row=7, column=1, padx=20, pady=5)

        self.difficulty_note = tk.Label(self.master, text="Remember to start a new game \nafter changing the difficulty", font=("Helvetica", 12))
        self.difficulty_note.grid(row=8, column=1, padx=20, pady=10)

        # Configure the grid to expand properly
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        for i in range(6):
            self.master.grid_rowconfigure(i, weight=1)

    def select_difficulty(self):
        difficulty = self.difficulty_var.get()
        if difficulty == "Easy":
            return 1, 10
        elif difficulty == "Medium":
            return 1, 100
        elif difficulty == "Hard":
            return 1, 1000

    def start_new_game(self):
        self.min_val, self.max_val = self.select_difficulty()
        self.number_to_guess = random.randint(self.min_val, self.max_val)
        self.attempts = 0
        self.max_attempts = 10
        self.game_mode_text.config(text=f"Guess a number between {self.min_val} and {self.max_val}")
        self.number_label.config(text="Number: ?")
        self.feedback_label.config(text="")
        self.attempts_counter.config(text=f"Attempts left: {self.max_attempts}")
        self.entry.config(state=tk.NORMAL)
        self.entry.delete(0, tk.END)


    def end_the_game(self, feedback, attempts):
        self.game_mode_text.config(text="Game Over! Start a new game")
        self.feedback_label.config(text=feedback)
        self.attempts_counter.config(text=f"Attempts left: {self.max_attempts - attempts}")
        self.number_label.config(text=f"Number: {self.number_to_guess}")
        self.entry.config(state=tk.DISABLED)
    def check_guess(self):
        guess_text = self.entry.get()
        if not guess_text.isdigit():
            self.feedback_label.config(text="Please enter a valid number!")
            self.entry.delete(0, tk.END)
            return

        self.attempts += 1

        guess = int(guess_text)


        if guess < self.number_to_guess:
            feedback = "Too low!"
            if abs(guess - self.number_to_guess) > 10:
                feedback += " and very cold!"
            else:
                feedback += " but getting warm!"
        elif guess > self.number_to_guess:
            feedback = "Too high!"
            if abs(guess - self.number_to_guess) > 10:
                feedback += " and very cold!"
            else:
                feedback += " but getting warm!"
        else:
            feedback = f"Congratulations! You guessed the number in {self.attempts} attempts!"
            self.number_label.config(text=f"Number: {self.number_to_guess}")
            if self.best_score is None or self.attempts < self.best_score:
                self.best_score = self.attempts
                self.best_score_label.config(text=f"Best Score: {self.best_score} attempts")
            self.end_the_game(feedback, self.attempts)
            return

        if self.attempts == self.max_attempts and guess != self.number_to_guess:
            feedback = f"Sorry, you've used all {self.max_attempts} attempts. \nThe number was {self.number_to_guess}. Better luck next time!"
            self.number_label.config(text=f"Number: {self.number_to_guess}")
            self.end_the_game(feedback, self.attempts)

        self.feedback_label.config(text=feedback)
        self.attempts_counter.config(text=f"Attempts left: {self.max_attempts - self.attempts}")
        self.entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    game = GuessTheNumberGame(root)
    root.mainloop()
