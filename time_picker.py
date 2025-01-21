import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class DateTimePicker:
    def __init__(self, parent):
        self.parent = parent
        self.top = tk.Toplevel(parent)
        self.top.title("Select Time")
        self.top.geometry("300x250")
        self.top.resizable(False, False)  # Make the window not resizable

        # Set the window icon
        self.set_icon()

        # Center the window on the screen
        self.center_window()

        self.start_time_var = tk.StringVar()
        self.end_time_var = tk.StringVar()

        tk.Label(self.top, text="Start Time (HH:MM)").pack(pady=5)
        self.start_time_entry = ttk.Combobox(self.top, textvariable=self.start_time_var, values=self.generate_time_options())
        self.start_time_entry.pack(pady=5)

        tk.Label(self.top, text="End Time (HH:MM)").pack(pady=5)
        self.end_time_entry = ttk.Combobox(self.top, textvariable=self.end_time_var, values=self.generate_time_options())
        self.end_time_entry.pack(pady=5)

        tk.Button(self.top, text="Next", command=self.on_next).pack(pady=20)

    def set_icon(self):
        # Load the icon image
        icon_image = Image.open("Assets/images/PUPLogo.png")
        icon_photo = ImageTk.PhotoImage(icon_image)
        self.top.iconphoto(False, icon_photo)

    def center_window(self):
        self.top.update_idletasks()
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        x = (self.top.winfo_screenwidth() // 2) - (width // 2)
        y = (self.top.winfo_screenheight() // 2) - (height // 2)
        self.top.geometry(f'{width}x{height}+{x}+{y}')

    def generate_time_options(self):
        times = []
        for hour in range(24):
            for minute in (0, 30):
                times.append(f"{hour:02}:{minute:02}")
        return times

    def on_next(self):
        start_time = self.start_time_var.get()
        end_time = self.end_time_var.get()
        if start_time and end_time:
            self.selected_datetime = f"{start_time} - {end_time}"
            self.top.destroy()
        else:
            tk.messagebox.showerror("Error", "Please select both start and end times.")

class SectionPicker:
    def __init__(self, parent, selected_datetime):
        self.parent = parent
        self.top = tk.Toplevel(parent)
        self.top.title("Select Program and Year Section")
        self.top.geometry("300x250")
        self.top.resizable(False, False)  # Make the window not resizable

        # Set the window icon
        self.set_icon()

        # Center the window on the screen
        self.center_window()

        self.selected_program = tk.StringVar()
        self.selected_year_section = tk.StringVar()

        self.program_data = ["BSIT", "BSIE", "BSECE"]
        tk.Label(self.top, text="Select Program").pack(pady=5)
        self.program_entry = ttk.Combobox(self.top, textvariable=self.selected_program, values=self.program_data)
        self.program_entry.pack(pady=5)

        self.year_section_data = ["1-1", "1-2", "2-1", "2-2", "3-1", "3-2", "4-1"]
        tk.Label(self.top, text="Select Year and Section").pack(pady=5)
        self.year_section_entry = ttk.Combobox(self.top, textvariable=self.selected_year_section, values=self.year_section_data)
        self.year_section_entry.pack(pady=5)

        tk.Button(self.top, text="Submit", command=self.on_submit).pack(pady=20)

    def set_icon(self):
        # Load the icon image
        icon_image = Image.open("Assets/images/PUPLogo.png")
        icon_photo = ImageTk.PhotoImage(icon_image)
        self.top.iconphoto(False, icon_photo)

    def center_window(self):
        self.top.update_idletasks()
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        x = (self.top.winfo_screenwidth() // 2) - (width // 2)
        y = (self.top.winfo_screenheight() // 2) - (height // 2)
        self.top.geometry(f'{width}x{height}+{x}+{y}')

    def on_submit(self):
        if self.selected_program.get() and self.selected_year_section.get():
            self.top.destroy()
        else:
            tk.messagebox.showerror("Error", "Please select both program and year section.")
