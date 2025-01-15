import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class ReservationPage:
    def __init__(self, root, colors, selected_day, go_back_callback):
        self.root = root
        self.colors = colors
        self.selected_day = selected_day
        self.go_back_callback = go_back_callback
        self.queue_info = tk.StringVar()
        self.queue_info.set("Program:\nYear and Sec.:")
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
        back_button.grid(row=0, column=0, padx=20, pady=20, sticky='nw')

        # Add Rooms section
        rooms_frame = tk.Frame(self.main_frame, bg=self.colors['white'], width=200, padx=10, pady=10, relief="solid", borderwidth=2)
        rooms_frame.grid(row=1, column=0, rowspan=2, sticky='ns')

        rooms_label = tk.Label(rooms_frame, text="Rooms", font=("Arial", 14), fg=self.colors['pup_maroon'], bg=self.colors['white'])
        rooms_label.pack(anchor="center", pady=10)

        # Add more widgets to the rooms frame as needed
        rooms_info_label = tk.Label(rooms_frame, text="Room details here", font=("Arial", 12), bg=self.colors['white'])
        rooms_info_label.pack(pady=6, fill="x")

        # Create a frame for the center content
        center_frame = tk.Frame(self.main_frame, bg=self.colors['white'])
        center_frame.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

        # Add more widgets to the center frame as needed
        center_label = tk.Label(center_frame, text="New \nBuilding", bg=self.colors['white'], fg=self.colors['pup_maroon'], font=('Arial', 40), justify='left')
        center_label.grid(row=0, column=0, padx=20, pady=20, sticky='w')

        # Add building image to the right side of the center label
        self.load_building_image(center_frame, row=0, column=1)

        # Draw underline below the center label
        self.draw_underline(center_frame, 200, row=1, column=0, columnspan=2)

        # Display the selected day
        self.display_date(center_frame, self.selected_day, row=2, column=0, columnspan=2)

        # Draw long underline
        self.draw_underline(center_frame, 700, row=3, column=0, columnspan=2)

        # Display available schedules label at the bottom of the long underline
        available_sched_label = tk.Label(center_frame, text="AVAILABLE SCHEDULE", bg=self.colors['white'], fg=self.colors['pup_maroon'], font=('Arial', 25))
        available_sched_label.grid(row=4, column=0, padx=20, pady=20, sticky='w', columnspan=2)

        # Create schedule table
        self.create_schedule_table(center_frame, row=5, column=0, columnspan=2)

        # Create queue frame
        self.create_queue_frame()

        # Configure grid weights
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        center_frame.grid_columnconfigure(0, weight=1)
        center_frame.grid_columnconfigure(1, weight=1)

    def draw_underline(self, parent, length, row, column, columnspan=1):
        # Create a canvas to draw the underline
        underline_canvas = tk.Canvas(parent, bg=self.colors['white'], height=2, bd=0, highlightthickness=0)
        underline_canvas.grid(row=row, column=column, columnspan=columnspan, sticky='ew', padx=20)
        underline_canvas.create_line(0, 0, length, 0, fill=self.colors['pup_maroon'], width=2)

    def display_date(self, parent, selected_day, row, column, columnspan=1):
        self.dates = {
            'MON': 'Monday',
            'TUE': 'Tuesday',
            'WED': 'Wednesday',
            'THU': 'Thursday',
            'FRI': 'Friday',
            'SAT': 'Saturday',
        }
        day_text = self.dates.get(selected_day, "Unknown Day")
        self.selected_day_label = tk.Label(parent, text=day_text, bg=self.colors['white'], fg=self.colors['pup_maroon'], font=('Arial', 20), justify='left')
        self.selected_day_label.grid(row=row, column=column, columnspan=columnspan, padx=20, pady=10, sticky='w')

    def create_schedule_table(self, content_frame, row, column, columnspan=1):
        columns = ("Time", "Program", "Year and Sec.", "No. of section in queue")
        self.schedule_table = ttk.Treeview(content_frame, columns=columns, show="headings", height=10, style="Bold.Treeview")
        for col in columns:
            self.schedule_table.heading(col, text=col)
            self.schedule_table.column(col, anchor="center", width=200)
        self.schedule_table.grid(row=row, column=column, columnspan=columnspan, pady=9, sticky='nsew')

        style = ttk.Style()
        style.configure("Bold.Treeview.Heading", font=("Tahoma", 12, "bold"), bg="#4A0202")

    def load_building_image(self, parent, row, column):
        try:
            building_image_path = "Assets/images/NBROOMS2.png"
            building_image = Image.open(building_image_path)
            building_image = building_image.resize((400, 250))
            self.building_image = ImageTk.PhotoImage(building_image)
            building_image_label = tk.Label(parent, image=self.building_image, bg=self.colors['white'])
            building_image_label.grid(row=row, column=column, padx=10, pady=10, sticky='ne')
        except FileNotFoundError:
            tk.Label(parent, text="Building image not found", bg=self.colors['white']).grid(row=row, column=column, padx=10, pady=10, sticky='ne')

    def create_queue_frame(self):
        queue_frame = tk.Frame(self.main_frame, bg="#4A0202", width=200, height=400, padx=10, pady=10, relief="solid", borderwidth=2)
        queue_frame.grid(row=1, column=2, rowspan=2, sticky='ns')

        queue_label = tk.Label(queue_frame, text="Queue", font=("Arial", 14), fg="#E0E0E0", bg="#4A0202")
        queue_label.pack(anchor="center", pady=10)

        queue_info_label = tk.Label(
            queue_frame,
            textvariable=self.queue_info,
            font=("Arial", 12),
            width=25,
            height=2,
            wraplength=180
        )
        queue_info_label.pack(pady=6, fill="x")

        self.load_logo_image(queue_frame)

    def load_logo_image(self, queue_frame):
        try:
            logo_path = "Assets/images/nb.jpg"
            logo_image = tk.PhotoImage(file=logo_path)
            logo_image = logo_image.subsample(3, 3)
            logo_label = tk.Label(queue_frame, image=logo_image)
            logo_label.image = logo_image
            logo_label.pack(side="bottom", pady=10)
        except tk.TclError:
            tk.Label(queue_frame, text="Logo not found", bg="#E0E0E0").pack(side="bottom", pady=10)

    def go_back(self):
        # Clear the current frame
        for widget in self.root.winfo_children():
            widget.destroy()

        # Call the callback function to return to the homepage
        self.go_back_callback()

    def run(self):
        self.root.mainloop()