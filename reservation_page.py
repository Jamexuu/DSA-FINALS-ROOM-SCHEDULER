import tkinter as tk
from PIL import Image, ImageTk

class ReservationPage:
    def __init__(self, root, colors, selected_day, go_back_callback):
        self.root = root
        self.colors = colors
        self.selected_day = selected_day
        self.go_back_callback = go_back_callback
        self.setup_gui()

    def setup_gui(self):
        self.main_frame = tk.Frame(self.root, bg=self.colors['white'])
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Load the back button icon
        back_icon = Image.open("Assets/images/back_button.png")
        back_icon = back_icon.resize((30, 30))  # Resize the icon if needed
        self.back_icon_photo = ImageTk.PhotoImage(back_icon)

        # Add back button with icon
        back_button = tk.Button(self.main_frame, image=self.back_icon_photo, command=self.go_back, bg=self.colors['white'], borderwidth=0)
        back_button.pack(anchor='nw', padx=20, pady=20)

        # Create three vertical frames with borders
        self.left_frame = tk.Frame(self.main_frame, bg=self.colors['white'], width=250, bd=2, relief="solid")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        self.center_frame = tk.Frame(self.main_frame, bg=self.colors['white'], width=600, bd=2, relief="solid")
        self.center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = tk.Frame(self.main_frame, bg=self.colors['white'], width=350, bd=2, relief="solid")
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        # Add more widgets to each frame as needed
        left_label = tk.Label(self.left_frame, text="Rooms", bg=self.colors['white'], font=('Arial', 16))
        left_label.pack(pady=20)

        center_label = tk.Label(self.center_frame, text="New \nBuilding", bg=self.colors['white'], fg=self.colors['pup_maroon'], font=('Arial', 40), justify='left')
        center_label.pack(anchor='w', padx=20, pady=20)

        # Draw underline below the center label
        self.draw_underline(self.center_frame, 200)

        # Display the selected day
        self.display_date(self.selected_day)

        # Draw long underline
        self.draw_underline(self.center_frame, 700)

        # Display available schedules label at the bottom of the long underline
        available_sched_label = tk.Label(self.center_frame, text="AVAILABLE SCHEDULE", bg=self.colors['white'], font=('Arial', 30))
        available_sched_label.pack(anchor='w', padx=20, pady=20)

        right_label = tk.Label(self.right_frame, text="Queue", bg=self.colors['white'], font=('Arial', 16))
        right_label.pack(pady=20)

    def draw_underline(self, parent, length):
        # Create a canvas to draw the underline
        underline_canvas = tk.Canvas(parent, bg=self.colors['white'], height=2, bd=0, highlightthickness=0)
        underline_canvas.pack(fill='x', padx=20)
        underline_canvas.create_line(0, 0, length, 0, fill=self.colors['pup_maroon'], width=2)

    def display_date(self, selected_day):
        self.dates = {
            'MON': 'Monday',
            'TUE': 'Tuesday',
            'WED': 'Wednesday',
            'THU': 'Thursday',
            'FRI': 'Friday',
            'SAT': 'Saturday',
        }
        day_text = self.dates.get(selected_day, "Unknown Day")
        self.selected_day_label = tk.Label(self.center_frame, text=day_text, bg=self.colors['white'], font=('Arial', 16))
        self.selected_day_label.pack(anchor='w', padx=10, pady=10)

    def go_back(self):
        # Clear the current frame
        for widget in self.root.winfo_children():
            widget.destroy()

        # Call the callback function to return to the homepage
        self.go_back_callback()

    def run(self):
        self.root.mainloop()