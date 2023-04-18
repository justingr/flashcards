import random
import glob
import tkinter as tk
from tkinter import messagebox
import os
import simpleaudio as sa
from PIL import Image, ImageTk

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
        self.current_operation = None
        self.title("Flashcard App")
        self.geometry("800x800")
        #self.resizable(False, False)  # Disable window resizing

        background_image = Image.open('assets/background.png')
        self.background_image = ImageTk.PhotoImage(background_image)

        self.operation = tk.StringVar()
        self.operation.set("multiplication")
        self.create_widgets()
        self.center_window()

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (800 // 2)
        y = (screen_height // 2) - (800 // 2)

        self.geometry(f"800x800+{x}+{y}")
    

    def play_correct_sound(self):
        correct_sound_file = "assets/correct_sound.wav"
        if os.path.exists(correct_sound_file):
            wave_obj = sa.WaveObject.from_wave_file(correct_sound_file)
            wave_obj.play()
        else:
            print("Sound file not found")

    def play_incorrect_sound(self):
        incorrect_sound_file = "assets/incorrect_sound.wav"
        if os.path.exists(incorrect_sound_file):
            wave_obj = sa.WaveObject.from_wave_file(incorrect_sound_file)
            wave_obj.play()
        else:
            print("Sound file not found")

    def create_widgets(self):
        bg_color = "#a7baa6"
        self.operation_buttons_frame = tk.Frame(self, bg=bg_color)
        self.operation_buttons_frame.pack(pady=20)

        for operation in ["addition", "subtraction", "multiplication", "division"]:
            operation_button = tk.Button(self.operation_buttons_frame, text=operation.capitalize(),
                                        command=lambda op=operation: self.start_flashcard(operation=op),
                                        bg=bg_color, fg="black", highlightbackground=bg_color,
                                        bd=0, relief="ridge")
            operation_button.pack(side=tk.LEFT, padx=10)

        self.question_label = tk.Label(self, text="", font=("Helvetica", 100, "bold"), bg=bg_color)
        self.question_label.pack(pady=20)
        self.answer_entry = tk.Entry(self, font=("Helvetica", 100, "bold"), width=3, bg=bg_color)
        self.answer_entry.pack()
        self.submit_button = tk.Button(self, text="Submit", command=self.check_answer, state="disabled")
        self.submit_button.pack()

        # Bind the Return key to the check_answer function
        self.bind("<Return>", lambda event: self.check_answer())
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Bring the other widgets to the front
        self.operation_buttons_frame.lift()
        self.question_label.lift()
        self.answer_entry.lift()
        self.submit_button.lift()

    def start_flashcard(self, operation):
        self.current_operation = operation
        self.question, self.answer = generate_flashcard(self.current_operation)
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
            self.start_flashcard(operation=self.current_operation) # Move this line here to only proceed to the next question when the answer is correct
        else:
            self.play_incorrect_sound()  # Play the incorrect sound

if __name__ == "__main__":
    app = FlashcardApp()
    app.mainloop()

