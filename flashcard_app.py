import glob
import random
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

        background_image = Image.open(self.get_random_background_image())
        self.background_image = ImageTk.PhotoImage(background_image)
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.bg_color = self.get_random_pixel_color(background_image)

        self.operation = tk.StringVar()
        self.operation.set("multiplication")
        self.create_widgets()
        self.center_window()

    def get_random_pixel_color(self, image):
        width, height = image.size
        random_x = random.randint(0, width - 1)
        random_y = random.randint(0, height - 1)
        pixel_color = image.getpixel((random_x, random_y))
        return "#{:02x}{:02x}{:02x}".format(pixel_color[0], pixel_color[1], pixel_color[2])


    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (800 // 2)
        y = (screen_height // 2) - (800 // 2)

        self.geometry(f"800x800+{x}+{y}")
    
    def get_random_background_image(self):
        background_images = glob.glob("assets/*.png")
        return random.choice(background_images)

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
        self.operation_buttons_frame = tk.Frame(self, bg=self.bg_color)
        self.operation_buttons_frame.pack(pady=20)

        for operation in ["addition", "subtraction", "multiplication", "division"]:
            operation_button = tk.Button(self.operation_buttons_frame, text=operation.capitalize(),
                                         command=lambda op=operation: self.start_flashcard(operation=op),
                                         bg=self.bg_color, fg="black", highlightbackground=self.bg_color,
                                         bd=0, relief="ridge")
            operation_button.pack(side=tk.LEFT, padx=10)

        self.question_label = tk.Label(self, text="", font=("Helvetica", 100, "bold"), bg=self.bg_color)
        self.question_label.pack(pady=20)
        self.answer_entry = tk.Entry(self, font=("Helvetica", 100, "bold"), width=3, bg=self.bg_color)
        self.answer_entry.pack()
        self.submit_button = tk.Button(self, text="Submit", command=self.check_answer, state="disabled")
        self.submit_button.pack()

        # Bind the Return key to the check_answer function
        self.bind("<Return>", lambda event: self.check_answer())

        # Bring the other widgets to the front
        self.operation_buttons_frame.lift()
        self.question_label.lift()
        self.answer_entry.lift()
        self.submit_button.lift()

    def start_flashcard(self, operation):
        self.operation.set(operation)
        self.question, self.answer = generate_flashcard(self.operation.get())
        self.question_label.config(text=self.question)
        self.answer_entry.delete(0, tk.END)
        self.submit_button.config(state="normal")

        background_image = Image.open(self.get_random_background_image())
        self.background_photo = ImageTk.PhotoImage(background_image)
        self.background_label.config(image=self.background_photo)


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

