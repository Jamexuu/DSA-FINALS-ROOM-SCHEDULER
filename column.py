import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class ScheduleApp:
    def __init__(self, root):
        self.root = root
        self.schedule_data = {}
        self.queue_info = tk.StringVar()
        self.queue_info.set("Program:\nYear and Sec.:")
        self.root.config(bg="#4A0202")
        self.setup_ui()

    def setup_ui(self):
        self.root.title("New Building Schedule")
        self.root.geometry("900x700")
        self.root.config(bg="#f4f4f4")

        self.create_rooms_frame()
        self.create_content_frame()
        self.create_queue_frame()

        self.update_schedule("NB 101")

    def create_rooms_frame(self):
        rooms_frame = tk.Frame(self.root, bg="#fff", width=300)
        rooms_frame.pack(side="left", fill="y")

        back_button = tk.Button(
            rooms_frame,
            text="← Back",
            font=("Arial", 12, "bold"),
            fg="#fff",
            bg="#a00",
            activebackground="#d00",
            command=self.back_to_main
        )
        back_button.pack(pady=10)

        rooms_label = tk.Label(rooms_frame, text="Rooms", font=("Arial", 14, "bold"), bg="#fff", fg="#a00")
        rooms_label.pack(pady=10)

        rooms_list = [
            "NB 101", "NB 102", "NB 103", "NB 104", "NB 203", "NB 204", "NB 205", "NB 206",
            "NB 301", "NB 302", "NB 303", "NB 304", "NB 305", "NB 306", "NB 401", "NB 402",
            "NB 403", "NB 404", "NB 405"
        ]

        rooms_listbox = tk.Listbox(rooms_frame, font=("Arial", 14), bg="#f4f4f4", activestyle="none", justify="center")
        rooms_listbox.pack(fill="both", expand=True, pady=4)

        for room in rooms_list:
            rooms_listbox.insert(tk.END, room)

        rooms_listbox.bind("<<ListboxSelect>>", lambda event: self.update_schedule(rooms_listbox.get(rooms_listbox.curselection())))

        scrollbar = tk.Scrollbar(rooms_frame, orient="vertical", command=rooms_listbox.yview)
        rooms_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def create_content_frame(self):
        content_frame = tk.Frame(self.root, bg="#E0E0E0", padx=10, pady=10)
        content_frame.pack(side="left", fill="both", expand=True)

        header_frame = tk.Frame(content_frame, bg="#E0E0E0")
        header_frame.pack(anchor="w", pady=(8, 8), fill="x")

        header_label = tk.Label(header_frame, text="New Building", font=("Roboto", 32, "bold"), bg="#E0E0E0", fg="#a00")
        header_label.pack(side="left")

        self.load_building_image(header_frame)

        separator = ttk.Separator(content_frame, orient="horizontal")
        separator.pack(fill="x", pady=(5, 0))
        style = ttk.Style()
        style.configure("TSeparator", background="black")

        schedule_label = tk.Label(content_frame, text="Available Schedule", font=("Helvetica", 14, "bold"), bg="#E0E0E0", fg="#a00")
        schedule_label.pack(anchor="w")

        self.create_schedule_table(content_frame)

    def load_building_image(self, header_frame):
        try:
            building_image_path ="Assets/images/NBROOMS2.png"
            building_image = Image.open(building_image_path)
            building_image = building_image.resize((400, 250))
            self.building_image = ImageTk.PhotoImage(building_image)
            building_image_label = tk.Label(header_frame, image=self.building_image, bg="#E0E0E0")
            building_image_label.image = self.building_image
            building_image_label.pack(side="right", padx=10)
        except FileNotFoundError:
            tk.Label(header_frame, text="Building image not found", bg="#E0E0E0").pack(side="right", padx=10)

    def create_schedule_table(self, content_frame):
        columns = ("Time", "Program", "Year and Sec.", "No. of section in queue")
        self.schedule_table = ttk.Treeview(content_frame, columns=columns, show="headings", height=10, style="Bold.Treeview")
        for col in columns:
            self.schedule_table.heading(col, text=col)
            self.schedule_table.column(col, anchor="center", width=250)
        self.schedule_table.pack(anchor="center", pady=9)

        style = ttk.Style()
        style.configure("Bold.Treeview.Heading", font=("Tahoma", 12, "bold"), bg="#4A0202")

    def create_queue_frame(self):
        queue_frame = tk.Frame(self.root, bg="#4A0202", width=200, padx=10, pady=10, relief="solid", borderwidth=2)
        queue_frame.pack(side="right", fill="y")

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

    def update_schedule(self, room):
        for row in self.schedule_table.get_children():
            self.schedule_table.delete(row)
        if room in self.schedule_data:
            for schedule in self.schedule_data[room]:
                self.schedule_table.insert("", "end", values=(schedule["time"], schedule["program"], schedule["yearSec"], schedule["queue"]))

    def update_queue(self, selected_schedule):
        if selected_schedule:
            self.queue_info.set(f"Program: {selected_schedule['program']}\nYear and Sec.: {selected_schedule['yearSec']}\nQueue: {selected_schedule['queue']}")
        else:
            self.queue_info.set("No schedule selected.")

    def back_to_main(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = ScheduleApp(root)
    root.mainloop()
