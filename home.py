import tkinter as tk
from PIL import Image, ImageTk
from reservation_page import ReservationPage

class HomePage:
    def __init__(self, root, colors, fonts):
        self.root = root
        self.fonts = fonts
        self.colors = colors
        self.setup_gui()

    def setup_gui(self):
        self.create_main_frame()
        self.create_title_label()
        self.create_days_grid(self.main_frame)
        self.create_sidebar()

    def create_main_frame(self):
        self.main_frame = tk.Frame(self.root, bg=self.colors['white'])
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def create_title_label(self):
        title_label = tk.Label(self.main_frame,
                               text="WEEKLY CALENDAR",
                               font=('Arial Black', 36, 'bold'),
                               bg=self.colors['white'],
                               fg="black")
        title_label.pack(pady=(40, 60))

    def create_circle_with_number(self, parent, number):
        canvas = tk.Canvas(parent, 
                           width=24, 
                           height=24, 
                           bg=self.colors['box_maroon'],
                           highlightthickness=0)
    
        # Draw white circle with white fill
        canvas.create_oval(2, 2, 22, 22, 
                           outline=self.colors['white'],
                           fill=self.colors['white'],  # Added white fill
                           width=1)
    
        # Add number (changed to maroon color)
        canvas.create_text(12, 12,
                           text=str(number),
                           fill=self.colors['box_maroon'],  # Changed to maroon
                           font=('Arial', 10, 'bold'))
    
        return canvas

    def create_days_grid(self, parent):
        # Create a canvas to hold the background image and buttons
        canvas = tk.Canvas(parent, bg=self.colors['white'])
        canvas.pack(fill="both", expand=True)

        # Draw the background image on the canvas
        def draw_logo():
            try:
                logo = Image.open("Assets/images/PUPLogo.png")
                logo = logo.resize((400, 400))
                logo.putalpha(50)  # 50% transparency
                self.logo_photo = ImageTk.PhotoImage(logo)
                canvas.create_image(canvas.winfo_width() // 2, canvas.winfo_height() // 2, image=self.logo_photo, anchor="center")
            except:
                pass

        canvas.after(100, draw_logo)  # Delay the drawing to ensure the canvas is rendered

        # Create the grid frame on top of the canvas
        def create_buttons():
            days = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
            button_width = 148
            button_height = 118
            gap_x = 90  # X Gap between buttons
            gap_y = 30  # Y Gap between buttons
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            x_offset = (canvas_width - (button_width * 3 + gap_x * 2)) // 2
            y_offset = (canvas_height - (button_height * 2 + gap_y)) // 2

            for i in range(2):
                for j in range(3):
                    index = i * 3 + j
                    if index < len(days):
                        x = x_offset + j * (button_width + gap_x)
                        y = y_offset + i * (button_height + gap_y)
                        self.create_day_box(canvas, days[index], index + 1, x, y, button_width, button_height)

        canvas.after(200, create_buttons)  # Delay the button creation to ensure the canvas is rendered

    def create_day_box(self, canvas, day, number, x, y, width, height):
        # Create a canvas for the rounded rectangle button
        button_canvas = tk.Canvas(canvas, width=width, height=height, bg=self.colors['white'], highlightthickness=0)
        button_canvas.place(x=x, y=y)

        # Draw the rounded rectangle
        radius = 20
        button_canvas.create_arc((0, 0, radius, radius), start=90, extent=90, fill=self.colors['box_maroon'], outline=self.colors['box_maroon'])
        button_canvas.create_arc((width-radius, 0, width, radius), start=0, extent=90, fill=self.colors['box_maroon'], outline=self.colors['box_maroon'])
        button_canvas.create_arc((0, height-radius, radius, height), start=180, extent=90, fill=self.colors['box_maroon'], outline=self.colors['box_maroon'])
        button_canvas.create_arc((width-radius, height-radius, width, height), start=270, extent=90, fill=self.colors['box_maroon'], outline=self.colors['box_maroon'])
        button_canvas.create_rectangle((radius//2, 0, width-radius//2, height), fill=self.colors['box_maroon'], outline=self.colors['box_maroon'])
        button_canvas.create_rectangle((0, radius//2, width, height-radius//2), fill=self.colors['box_maroon'], outline=self.colors['box_maroon'])

        # Create the day label on top of the rounded rectangle
        day_label = tk.Label(button_canvas, text=day, bg=self.colors['box_maroon'], fg=self.colors['white'], font=('Arial', 16, 'bold'))
        day_label.place(relx=0.5, rely=0.5, anchor='center')

        # Create and place circled number at the top right of the button
        circle_canvas = self.create_circle_with_number(button_canvas, number)
        circle_canvas.place(relx=0.80, rely=0.08)

        # Add hover effect
        self.add_hover_effect(button_canvas, day_label, circle_canvas)

        # Bind click event to navigate to reservation page
        button_canvas.bind("<Button-1>", lambda e: self.go_to_reservation_page(day))

    def add_hover_effect(self, button_canvas, day_label, circle_canvas):
        def on_enter(e):
            button_canvas.itemconfig("all", fill=self.colors['pup_dark_maroon'], outline=self.colors['pup_dark_maroon'])
            day_label.configure(bg=self.colors['pup_dark_maroon'])
            circle_canvas.configure(bg=self.colors['pup_dark_maroon'])

        def on_leave(e):
            button_canvas.itemconfig("all", fill=self.colors['box_maroon'], outline=self.colors['box_maroon'])
            day_label.configure(bg=self.colors['box_maroon'])
            circle_canvas.configure(bg=self.colors['box_maroon'])

        button_canvas.bind("<Enter>", on_enter)
        button_canvas.bind("<Leave>", on_leave)
        day_label.bind("<Enter>", on_enter)
        day_label.bind("<Leave>", on_leave)
        circle_canvas.bind("<Enter>", on_enter)
        circle_canvas.bind("<Leave>", on_leave)

    def go_to_reservation_page(self, day):
        # Clear the current frame
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Navigate to the reservation page
        reservation_page = ReservationPage(self.root, self.colors, day, self.setup_gui, self.fonts)
        reservation_page.run()

    def create_sidebar(self):
        sidebar = tk.Canvas(self.root, bg=self.colors['white'], width=120, height=600, highlightthickness=0)  # Increased height to 600
        sidebar.pack_propagate(False)  # Prevent the sidebar from resizing to fit its contents
        sidebar.pack(side=tk.RIGHT, fill=tk.Y, pady=(90, 70))  # Adjusted vertical padding

        # Draw rounded rectangle with only top left and bottom left corners rounded
        def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
            points = [
                x1 + radius, y1,
                x2, y1,
                x2, y1,
                x2, y1,
                x2, y1,
                x2, y2,
                x2, y2,
                x2, y2,
                x2, y2,
                x1 + radius, y2,
                x1, y2,
                x1, y2 - radius,
                x1, y1 + radius,
                x1, y1,
            ]
            return canvas.create_polygon(points, **kwargs, smooth=True)

        # Example usage of create_rounded_rectangle
        create_rounded_rectangle(sidebar, 10, 10, 110, 590, radius=45, fill=self.colors['pup_maroon'], outline=self.colors['pup_maroon'])  # Adjusted height to 590

