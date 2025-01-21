import tkinter as tk
from tkinter import ttk, messagebox, simpledialog  # Import simpledialog
from PIL import Image, ImageTk
from sort_room import RoomScheduler, get_rooms  # Import the RoomScheduler class and get_rooms function
from time_picker import DateTimePicker, SectionPicker
from queue_system import QueueManager  # Import the QueueManager class
import json

class ReservationPage:
    def __init__(self, root, colors, selected_day, go_back_callback, fonts):
        self.root = root
        self.colors = colors
        self.fonts = fonts
        self.selected_day = selected_day
        self.go_back_callback = go_back_callback
        self.queue_info = tk.StringVar()
        self.queue_info.set("Program")
        self.queue_info.set("Year and Sec.")
        self.current_selected_label = None
        self.selected_datetime = None
        self.selected_program = None
        self.selected_year_section = None
        self.queue_manager = QueueManager()  # Initialize the QueueManager
        self.current_room_name = None  # Store the current room name
        self.setup_gui()

    def setup_gui(self):
        self.main_frame = tk.Frame(self.root, bg=self.colors['white'])
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        top_bar = tk.Frame(self.main_frame, bg=self.colors['white'])
        top_bar.grid(row=0, column=0, columnspan=2, sticky='ew')

        back_icon = Image.open("Assets/images/back_button.png")
        back_icon = back_icon.resize((30, 30))
        self.back_icon_photo = ImageTk.PhotoImage(back_icon)

        back_button = tk.Button(top_bar, image=self.back_icon_photo, command=self.go_back, bg=self.colors['white'], borderwidth=0)
        back_button.pack(side=tk.LEFT, padx=10, pady=10)

        refresh_icon = Image.open("Assets/images/refresh.png")
        refresh_icon = refresh_icon.resize((28, 28))
        self.refresh_icon_photo = ImageTk.PhotoImage(refresh_icon)

        refresh_button = tk.Button(top_bar, image=self.refresh_icon_photo, command=self.refresh, bg=self.colors['white'], borderwidth=0)
        refresh_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.rooms_frame = tk.Frame(self.main_frame, bg=self.colors['white'], width=300, padx=10, pady=10, relief="solid", borderwidth=0)
        self.rooms_frame.grid(row=1, column=0, rowspan=2, sticky='ns')

        rooms_label = tk.Label(self.rooms_frame, text="Rooms", font=("Arial", 14), fg=self.colors['pup_maroon'], bg=self.colors['white'])
        rooms_label.pack(anchor="center", pady=10)

        center_frame = tk.Frame(self.main_frame, bg=self.colors['gray'])
        center_frame.grid(row=1, column=1, rowspan=2, sticky='nsew', padx=10, pady=10)

        center_label = tk.Label(center_frame, text="New \nBuilding", bg=self.colors['gray'], fg=self.colors['pup_maroon'], font=(self.fonts['gilroy heavy'], 40), justify='left')
        center_label.grid(row=0, column=0, padx=20, pady=(20, 0), sticky='w')

        self.draw_underline(center_frame, 200, row=0, column=0, columnspan=2, pady=(140,0))

        self.load_building_image(center_frame, row=0, column=1)

        self.display_date(center_frame, self.selected_day, row=0, column=0, columnspan=2)

        self.draw_underline(center_frame, 1230, row=0, column=0, columnspan=2, pady=(250, 0))

        schedule_icon = Image.open("Assets/images/schedule icon.png")
        schedule_icon = schedule_icon.resize((30, 30))
        self.schedule_icon_photo = ImageTk.PhotoImage(schedule_icon)

        schedule_icon_label = tk.Label(center_frame, image=self.schedule_icon_photo, bg=self.colors['gray'])
        schedule_icon_label.grid(row=4, column=0, padx=(15, 0), pady=20, sticky='w')

        available_sched_label = tk.Label(center_frame, text="AVAILABLE SCHEDULE", bg=self.colors['gray'], fg=self.colors['pup_maroon'], font=('Arial', 25))
        available_sched_label.grid(row=4, column=0, padx=(50, 0), pady=20, sticky='w', columnspan=2)

        select_time_button = tk.Button(center_frame, text="Add Date", command=self.select_time, bg=self.colors['pup_maroon'], fg=self.colors['white'])
        select_time_button.grid(row=4, column=1, padx=(200, 150), pady=20, sticky='e')

        terminate_schedule_button = tk.Button(center_frame, text="Terminate Schedule", command=self.terminate_schedule, bg=self.colors['pup_maroon'], fg=self.colors['white'])
        terminate_schedule_button.grid(row=4, column=1, padx=(250, 30), pady=20, sticky='e')

        self.create_schedule_table(center_frame, row=5, column=0, columnspan=2)

        self.create_queue_frame()

        self.main_frame.grid_columnconfigure(0, minsize=250)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        center_frame.grid_columnconfigure(0, weight=1)
        center_frame.grid_columnconfigure(1, weight=1)

        self.display_sorted_rooms()

    def draw_underline(self, parent, length, row, column, columnspan=1, pady=(0, 0)):
        underline_canvas = tk.Canvas(parent, bg=self.colors['gray'], height=2, bd=0, highlightthickness=0)
        underline_canvas.grid(row=row, column=column, columnspan=columnspan, sticky='ew', padx=20, pady=pady)
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
        self.selected_day_label = tk.Label(parent, text=day_text, bg=self.colors['gray'], fg=self.colors['pup_maroon'], font=('Arial', 20), justify='left')
        self.selected_day_label.grid(row=row, column=column, columnspan=columnspan, padx=20, pady=(180, 0), sticky='w')

    def create_schedule_table(self, content_frame, row, column, columnspan=1):
        columns = ("Time", "Program", "Year and Sec.")
        self.schedule_table = ttk.Treeview(
            content_frame,
            columns=columns,
            show="headings",
            height=10,
            style="Custom.Treeview"
        )

        for col in columns:
            self.schedule_table.heading(col, text=col)
            self.schedule_table.column(col, anchor="center", width=200)

        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Custom.Treeview.Heading",
            font=("Tahoma", 12, "bold"),
            background=self.colors['gray'],
            foreground=self.colors['black'],
            relief="raised"
        )

        style.configure(
            "Custom.Treeview",
            background=self.colors['gray'],
            foreground=self.colors['black'],
            fieldbackground=self.colors['gray'],
        )

        style.map(
            "Custom.Treeview",
            background=[('selected', self.colors['gray'])],
            foreground=[('selected', self.colors['black'])],
        )

        self.schedule_table.grid(row=row, column=column, columnspan=columnspan, pady=9, sticky='nsew')

        self.schedule_table.configure(style="Custom.Treeview")

    def load_building_image(self, parent, row, column):
        try:
            building_image_path = "Assets/images/NBROOMS2.png"
            building_image = Image.open(building_image_path)
            building_image = building_image.resize((600, 250))
            self.building_image = ImageTk.PhotoImage(building_image)
            building_image_label = tk.Label(parent, image=self.building_image, bg=self.colors['gray'])
            building_image_label.grid(row=row, column=column, padx=10, pady=10, sticky='ne')
        except FileNotFoundError:
            tk.Label(parent, text="Building image not found", bg=self.colors['gray']).grid(row=row, column=column, padx=10, pady=10, sticky='ne')

    def terminate_queue_schedule(self):
        room_name = self.current_room_name
        if not room_name:
            messagebox.showerror("Error", "No room selected.")
            return

        queue = self.queue_manager.get_queue(room_name)
        if not queue:
            messagebox.showinfo("Info", "No schedules in the queue to terminate.")
            return

        row_numbers = simpledialog.askstring("Terminate Queue Schedule", "Enter queue numbers to terminate (comma-separated):")
        if row_numbers:
            row_numbers = [int(num.strip()) for num in row_numbers.split(",") if num.strip().isdigit()]
            if not row_numbers:
                messagebox.showerror("Error", "Invalid queue numbers entered.")
                return

            confirm = messagebox.askyesno("Confirm Termination", "Are you sure you want to terminate the selected queue schedules?")
            if confirm:
                for row_num in sorted(row_numbers, reverse=True):
                    try:
                        entry = queue.pop(row_num - 1)
                        start_time, end_time, program, year_section = entry
                        self.remove_schedule_from_json(room_name, start_time, end_time, program, year_section)
                    except IndexError:
                        messagebox.showerror("Error", f"Queue number {row_num} is out of range.")
                        return

                self.queue_manager.save_queue_data()
                self.update_queue_display(room_name)
                messagebox.showinfo("Success", "Selected queue schedules have been terminated.")

    def remove_schedule_from_json(self, room_name, start_time, end_time, program, year_section):
        try:
            with open("room_scheduler_data.json", "r") as file:
                schedules = json.load(file)

            if room_name in schedules:
                schedules[room_name] = [entry for entry in schedules[room_name] if not (
                    entry[0] == start_time and
                    entry[1] == end_time and
                    entry[2] == program and
                    entry[3] == year_section
                )]

                with open("room_scheduler_data.json", "w") as file:
                    json.dump(schedules, file, indent=4)
        except FileNotFoundError:
            messagebox.showerror("Error", "Schedules file not found.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error decoding schedules file.")

    def create_queue_frame(self):
        self.queue_frame = tk.Frame(self.main_frame, bg=self.colors['gray'], width=300, height=500, padx=10, pady=10, relief="solid", borderwidth=0)
        self.queue_frame.grid(row=1, column=2, rowspan=2, sticky='ns', pady=(10, 10))
        self.queue_frame.pack_propagate(False)  # Prevent the frame from resizing based on its content

        queue_label_frame = tk.Frame(self.queue_frame, bg=self.colors['gray'])
        queue_label_frame.pack(anchor="nw", pady=10, padx=10)

        queue_icon = Image.open("Assets/images/queue icon.png")
        queue_icon = queue_icon.resize((30, 30))
        self.queue_icon_photo = ImageTk.PhotoImage(queue_icon)

        queue_icon_label = tk.Label(queue_label_frame, image=self.queue_icon_photo, bg=self.colors['gray'])
        queue_icon_label.pack(side="left", padx=5)

        queue_label = tk.Label(queue_label_frame, text="Queue", font=("Arial", 18), fg=self.colors['pup_maroon'], bg=self.colors['gray'])
        queue_label.pack(side="left")

        # Create a frame to hold the queue information
        self.queue_info_frame = tk.Frame(self.queue_frame, bg=self.colors['gray'])
        self.queue_info_frame.pack(pady=6, fill="x")

        self.program_container = tk.Frame(self.queue_info_frame, bg=self.colors['gray'])
        self.program_container.pack(side="left", padx=(0, 50))

        self.year_sec_container = tk.Frame(self.queue_info_frame, bg=self.colors['gray'])
        self.year_sec_container.pack(side="left", padx=(0, 50))

        self.time_container = tk.Frame(self.queue_info_frame, bg=self.colors['gray'])
        self.time_container.pack(side="left")

        program_label = tk.Label(self.program_container, text="Program", font=("Arial", 12), bg=self.colors['gray'], fg=self.colors['black'])
        program_label.pack(anchor="w")

        year_sec_label = tk.Label(self.year_sec_container, text="Year and Sec.", font=("Arial", 12), bg=self.colors['gray'], fg=self.colors['black'])
        year_sec_label.pack(anchor="w")

        time_label = tk.Label(self.time_container, text="Time", font=("Arial", 12), bg=self.colors['gray'], fg=self.colors['black'])
        time_label.pack(anchor="w")

        # Add the terminate queue schedule button above the image
        self.load_logo_image(self.queue_frame)

    def load_logo_image(self, queue_frame):
        try:
            logo_path = "Assets/images/pylon2022.jpg"
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((200, 120))  # Fixed size for the image
            self.logo_image = ImageTk.PhotoImage(logo_image)
            logo_label = tk.Label(queue_frame, image=self.logo_image, bg=self.colors['gray'])
            
            # Add the terminate queue schedule button above the image
            terminate_queue_button = tk.Button(queue_frame, text="Terminate Queue Schedule", command=self.terminate_queue_schedule, bg=self.colors['pup_maroon'], fg=self.colors['white'])
            terminate_queue_button.pack(side='bottom', pady=(10, 0))

            logo_label.pack(side='bottom', pady=(0, 10))
        except FileNotFoundError:
            tk.Label(queue_frame, text="Logo not found", bg="#4A0202").pack(side="bottom", pady=10)
    
    def display_sorted_rooms(self):
        rooms = get_rooms()

        scheduler = RoomScheduler(rooms)
        sorted_rooms = scheduler.sort_rooms_by_availability(self.selected_day, "10:00", "11:00")

        for widget in self.rooms_frame.winfo_children():
            widget.destroy()

        rooms_label = tk.Label(self.rooms_frame, text="Rooms", font=("Arial", 14), fg=self.colors['pup_maroon'], bg=self.colors['white'])
        rooms_label.pack(anchor="center", pady=10)

        for index, room in enumerate(sorted_rooms):
            room_label = tk.Label(self.rooms_frame, text=room.name, font=("Arial", 12), bg=self.colors['white'], fg=self.colors['black'], cursor="hand2")
            room_label.pack(anchor="w", pady=2)
            room_label.bind("<Button-1>", lambda e, r=room, l=room_label: self.update_schedule_table(r, l))

            if index == 0:
                self.update_schedule_table(room, room_label)

    def update_schedule_table(self, room, label):
        for row in self.schedule_table.get_children():
            self.schedule_table.delete(row)

        day_schedule = room.schedule.get(self.selected_day, [])
        for entry in day_schedule:
            start_time, end_time, program, year_section = entry
            time_range = f"{start_time} - {end_time}"
            self.schedule_table.insert("", "end", values=(time_range, program, year_section))

        if self.current_selected_label and self.current_selected_label.winfo_exists():
            self.current_selected_label.config(bg=self.colors['white'], fg=self.colors['black'])
        label.config(bg=self.colors['pup_maroon'], fg=self.colors['white'])
        self.current_selected_label = label

        # Update the current room name and queue display
        self.current_room_name = room.name
        self.update_queue_display(room.name)

    def select_time(self):
        datetime_picker = DateTimePicker(self.root)
        self.root.wait_window(datetime_picker.top)
        self.selected_datetime = datetime_picker.selected_datetime

        if self.selected_datetime:
            section_picker = SectionPicker(self.root, self.selected_datetime)
            self.root.wait_window(section_picker.top)
            self.selected_program = section_picker.selected_program
            self.selected_year_section = section_picker.selected_year_section

            # Automatically add to the schedule table
            self.add_time_to_table()

    def add_time_to_table(self):
        if self.selected_datetime and self.selected_program and self.selected_year_section:
            if self.current_selected_label is None:
                messagebox.showerror("Error", "Please select a room first.")
                return

            start_time, end_time = self.selected_datetime.split(" - ")
            room_name = self.current_selected_label.cget("text")
            scheduler = RoomScheduler(get_rooms())
            room = next((r for r in scheduler.rooms if r.name == room_name), None)
            if room:
                if room.is_available(self.selected_day, start_time, end_time):
                    room.add_schedule(self.selected_day, start_time, end_time, self.selected_program.get(), self.selected_year_section.get())
                    self.update_schedule_table(room, self.current_selected_label)
                else:
                    self.queue_manager.add_to_queue(room_name, start_time, end_time, self.selected_program.get(), self.selected_year_section.get())
                    messagebox.showinfo("Info", "Schedule conflict. Added to queue.")

            self.schedule_table.insert("", "end", values=(f"{start_time} - {end_time}", self.selected_program.get(), self.selected_year_section.get()))
            self.update_queue_display(room_name)

    def terminate_schedule(self):
        row_number = simpledialog.askstring("Terminate Schedule", "Enter the row number to terminate:")
        if row_number:
            try:
                row_number = int(row_number.strip())
            except ValueError:
                messagebox.showerror("Error", "Invalid row number entered.")
                return

            if row_number <= 0:
                messagebox.showerror("Error", "Row number must be greater than zero.")
                return

            confirm = messagebox.askyesno("Confirm Termination", "Are you sure you want to terminate the selected schedule?")
            if confirm:
                try:
                    item = self.schedule_table.get_children()[row_number - 1]
                    values = self.schedule_table.item(item, "values")
                    if len(values) == 3:
                        time_range, program, year_section = values
                        start_time, end_time = time_range.split(" - ")
                        self.schedule_table.delete(item)
                        self.remove_schedule_from_json(self.current_room_name, start_time, end_time, program, year_section)
                    else:
                        messagebox.showerror("Error", f"Row number {row_number} does not contain the expected number of values.")
                        return
                except IndexError:
                    messagebox.showerror("Error", f"Row number {row_number} is out of range.")
                    return

                messagebox.showinfo("Success", "Selected schedule has been terminated.")

    def update_queue_display(self, room_name):
        for widget in self.program_container.winfo_children():
            widget.destroy()
        for widget in self.year_sec_container.winfo_children():
            widget.destroy()
        for widget in self.time_container.winfo_children():
            widget.destroy()

        queue = self.queue_manager.get_queue(room_name)
        for entry in queue:
            start_time, end_time, program, year_section = entry
            time_range = f"{start_time} - {end_time}"

            program_label = tk.Label(self.program_container, text=program, font=("Arial", 12), bg=self.colors['gray'], fg=self.colors['black'])
            program_label.pack(anchor="w", pady=2)

            year_sec_label = tk.Label(self.year_sec_container, text=year_section, font=("Arial", 12), bg=self.colors['gray'], fg=self.colors['black'])
            year_sec_label.pack(anchor="w", pady=2)

            time_label = tk.Label(self.time_container, text=time_range, font=("Arial", 12), bg=self.colors['gray'], fg=self.colors['black'])
            time_label.pack(anchor="w", pady=2)

    def refresh(self):
        self.display_sorted_rooms()
        if self.current_selected_label:
            room_name = self.current_selected_label.cget("text")
            scheduler = RoomScheduler(get_rooms())
            room = next((r for r in scheduler.rooms if r.name == room_name), None)
            if room:
                self.update_schedule_table(room, self.current_selected_label)
                self.update_queue_display(room_name)
        elif self.current_room_name:
            self.update_queue_display(self.current_room_name)

    def go_back(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.go_back_callback()

    def run(self):
        self.root.mainloop()