import random
import tkinter as tk
from tkinter import messagebox
import os
import simpleaudio as sa



def generate_flashcard(operation, min_value=1, max_value=12):
    if operation == "addition":
        a = random.randint(min_value, max_value)
        b = random.randint(min_value, max_value)
        question = f"{a} + {b} = ?"
        answer = a + b
    elif operation == "subtraction":
        a = random.randint(min_value, max_value)
        b = random.randint(min_value, min(a, 20))
        question = f"{a} - {b} = ?"
        answer = a - b
    elif operation == "multiplication":
        a = random.randint(min_value, max_value)
        b = random.randint(min_value, max_value)
        question = f"{a} × {b} = ?"
        answer = a * b
    elif operation == "division":
        b = random.randint(min_value, max_value)
        a = b * random.randint(min_value, max_value)
        question = f"{a} ÷ {b} = ?"
        answer = a // b
    else:
        raise ValueError("Invalid operation")
    return question, answer

class FlashcardApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Flashcard App")
        self.geometry("300x200")

        self.operation = tk.StringVar()
        self.operation.set("multiplication")

        self.create_widgets()

    def play_correct_sound(self):
        correct_sound_file = "correct_sound.wav"
        if os.path.exists(correct_sound_file):
            wave_obj = sa.WaveObject.from_wave_file(correct_sound_file)
            wave_obj.play()
        else:
            print("Sound file not found")

    def play_incorrect_sound(self):
        incorrect_sound_file = "incorrect_sound.wav"
        if os.path.exists(incorrect_sound_file):
            wave_obj = sa.WaveObject.from_wave_file(incorrect_sound_file)
            wave_obj.play()
        else:
            print("Sound file not found")


    def create_widgets(self):
        self.operation_label = tk.Label(self, text="Operation:")
        self.operation_label.pack()

        self.operation_menu = tk.OptionMenu(self, self.operation, "addition", "subtraction", "multiplication", "division")
        self.operation_menu.pack()

        self.start_button = tk.Button(self, text="Start", command=self.start_flashcard)
        self.start_button.pack()

        # Update the font size and style for the question_label
        self.question_label = tk.Label(self, text="", font=("Helvetica", 100, "bold"))
        self.question_label.pack()

        # Update the font size and style for the answer_entry
        self.answer_entry = tk.Entry(self, font=("Helvetica", 100, "bold"))
        self.answer_entry.pack()

        self.submit_button = tk.Button(self, text="Submit", command=self.check_answer, state="disabled")
        self.submit_button.pack()
       
        # Bind the Return key to the check_answer function
        self.bind("<Return>", lambda event: self.check_answer())


    def start_flashcard(self):
        self.question, self.answer = generate_flashcard(self.operation.get())
        self.question_label.config(text=self.question)
        self.answer_entry.delete(0, tk.END)
        self.submit_button.config(state="normal")

    def check_answer(self):
        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input")
            return

        if user_answer == self.answer:
            self.play_correct_sound()
            self.start_flashcard()  # Move this line here to only proceed to the next question when the answer is correct
        else:
            self.play_incorrect_sound()  # Play the incorrect sound

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Flashcard App")
        self.geometry("800x600")  # Set the initial window size
        #self.resizable(False, False)  # Disable window resizing

        self.operation = tk.StringVar(self)
        self.operation.set("addition")

        self.create_widgets()



if __name__ == "__main__":
    app = FlashcardApp()
    app.mainloop()
