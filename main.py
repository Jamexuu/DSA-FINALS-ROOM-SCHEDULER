import tkinter as tk
from home import HomePage
from PIL import Image, ImageTk

class PUPWeeklyCalendar:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PUP Weekly Calendar")
        self.root.geometry("1200x700")
        self.root.state('zoomed')  # Start in full-screen mode
        
        # Colors
        self.colors = {
            'pup_maroon': "#800000",  # Sidebar maroon
            'pup_dark_maroon': "#4A0404",  # Dark maroon for boxes
            'box_maroon': "#800000",  # Slightly lighter maroon for day boxes
            'white': "#FFFFFF",
            'black': "#000000"
        }
        
        self.root.configure(bg=self.colors['white'])
        self.set_icon()
        self.setup_gui()

    def set_icon(self):
        # Load the icon image
        icon_image = Image.open("Assets/images/PUPLogo.png")
        icon_photo = ImageTk.PhotoImage(icon_image)
        self.root.iconphoto(False, icon_photo)

    def setup_gui(self):
        self.home_page = HomePage(self.root, self.colors)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PUPWeeklyCalendar()
    app.run()